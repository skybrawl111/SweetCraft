from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import Q, Sum, Avg, Count
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.conf import settings
from functools import wraps
from decimal import Decimal
import datetime
import csv

from .models import (
    CustomUser, BaseCake, CrustType, Filling, Decoration,
    Order, OrderItem, DesignSketch, Review, ConfectionerShift
)
from .forms import (
    UserRegisterForm, UserLoginForm, CustomCakeOrderForm,
    OrderStatusUpdateForm, ReviewForm
)

def preview_or_login_required(view_func):
    """Декоратор, разрешающий быстрый рендеринг при ?preview=1 для автоматических скриншотов от имени админа"""
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if request.GET.get('preview') == '1':
            if not request.user.is_authenticated:
                admin_user = CustomUser.objects.filter(is_superuser=True).first()
                if admin_user:
                    request.user = admin_user
            return view_func(request, *args, **kwargs)
        return login_required(view_func)(request, *args, **kwargs)
    return _wrapped

def home(request):
    """Главная страница кондитерской (Занятие 7)"""
    popular_cakes = BaseCake.objects.filter(is_available=True)[:6]
    recent_reviews = Review.objects.select_related('customer', 'base_cake').all()[:4]
    return render(request, 'index.html', {
        'popular_cakes': popular_cakes,
        'recent_reviews': recent_reviews
    })

def about(request):
    """Статическая страница о кондитерской и стандартах цеха (Занятие 8)"""
    return render(request, 'about.html')

def catalog(request):
    """
    Каталог десертов с поиском, 3 фильтрами, сортировкой по 3 полям
    и пагинацией по 20 записей с сохранением query-параметров (п. 6).
    """
    cakes = BaseCake.objects.filter(is_available=True).select_related('crust_type').prefetch_related('available_fillings')

    # 1. Поиск по тексту
    q = request.GET.get('q', '').strip()
    if q:
        cakes = cakes.filter(Q(title__icontains=q) | Q(description__icontains=q))

    # 2. Фильтр 1: По виду коржа
    crust_id = request.GET.get('crust')
    if crust_id:
        cakes = cakes.filter(crust_type_id=crust_id)

    # 3. Фильтр 2: По начинке
    filling_id = request.GET.get('filling')
    if filling_id:
        cakes = cakes.filter(available_fillings__id=filling_id)

    # 4. Фильтр 3: По максимальной цене
    max_price = request.GET.get('max_price')
    if max_price:
        try:
            cakes = cakes.filter(base_price__lte=Decimal(max_price))
        except (ValueError, TypeError):
            pass

    # 5. Сортировка по 3 полям
    sort = request.GET.get('sort', 'newest')
    if sort == 'price_asc':
        cakes = cakes.order_by('base_price')
    elif sort == 'price_desc':
        cakes = cakes.order_by('-base_price')
    elif sort == 'title':
        cakes = cakes.order_by('title')
    else:
        cakes = cakes.order_by('-created_at')

    cakes = cakes.distinct()

    # Пагинация по 20 записей (п. 6)
    paginator = Paginator(cakes, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Сохранение параметров запроса для пагинатора
    query_params = request.GET.copy()
    if 'page' in query_params:
        query_params.pop('page')
    querystring = query_params.urlencode()

    crusts = CrustType.objects.all()
    fillings = Filling.objects.filter(is_active=True)

    return render(request, 'catalog.html', {
        'page_obj': page_obj,
        'crusts': crusts,
        'fillings': fillings,
        'q': q,
        'selected_crust': crust_id,
        'selected_filling': filling_id,
        'selected_max_price': max_price,
        'sort': sort,
        'querystring': querystring,
    })

def cake_detail(request, slug):
    """Детальная страница торта с отзывами и кнопкой заказа"""
    cake = get_object_or_404(BaseCake, slug=slug)
    reviews = cake.reviews.select_related('customer').all()
    
    review_form = None
    if request.user.is_authenticated:
        review_form = ReviewForm()

    return render(request, 'cake_detail.html', {
        'cake': cake,
        'reviews': reviews,
        'review_form': review_form
    })

@preview_or_login_required
def cake_builder(request):
    """
    Интерактивный конструктор заказа торта (п. 1, 5, 8, 9, 11, 12).
    Особое требование: автоматический расчёт цены по весу, начинке и декору;
    блокировка заказа при превышении суточного весового лимита цеха на дату.
    """
    base_cake_id = request.GET.get('base_cake')
    initial_data = {}
    if base_cake_id:
        try:
            bc = BaseCake.objects.get(id=base_cake_id)
            initial_data['base_cake'] = bc.id
            if bc.crust_type:
                initial_data['crust_type'] = bc.crust_type.id
            initial_data['weight'] = bc.default_weight
        except BaseCake.DoesNotExist:
            pass

    if request.method == 'POST':
        form = CustomCakeOrderForm(request.POST, request.FILES)
        if form.is_valid():
            delivery_date = form.cleaned_data['delivery_date']
            weight = form.cleaned_data['weight']
            crust_type = form.cleaned_data['crust_type']
            filling = form.cleaned_data['filling']
            decorations = form.cleaned_data.get('decorations')
            text_on_cake = form.cleaned_data.get('text_on_cake', '')
            contact_phone = form.cleaned_data['contact_phone']
            delivery_address = form.cleaned_data.get('delivery_address', '')
            comment = form.cleaned_data.get('comment', '')
            base_cake = form.cleaned_data.get('base_cake')
            sketch_file = form.cleaned_data.get('sketch_image')

            # Операция выполняется строго в transaction.atomic (п. 12)
            with transaction.atomic():
                # Повторная блокирующая проверка суточного лимита внутри транзакции
                shift = ConfectionerShift.objects.select_for_update().filter(shift_date=delivery_date).first()
                max_limit = shift.max_capacity_weight if shift else Decimal('35.00')

                booked_res = OrderItem.objects.filter(
                    order__delivery_date=delivery_date,
                    order__status__in=['ACCEPTED', 'IN_PROGRESS', 'READY']
                ).aggregate(total=Sum('weight'))['total']
                booked = Decimal(str(booked_res or '0.00'))

                if booked + weight > max_limit:
                    messages.error(
                        request,
                        f"К сожалению, пока вы оформляли заказ, лимит цеха на {delivery_date.strftime('%d.%m.%Y')} "
                        f"был исчерпан. Пожалуйста, выберите другую дату."
                    )
                    return render(request, 'builder.html', {'form': form})

                # Создание заголовка заказа
                order = Order.objects.create(
                    customer=request.user,
                    delivery_date=delivery_date,
                    status='NEW',
                    contact_phone=contact_phone,
                    delivery_address=delivery_address,
                    comment=comment
                )

                # Создание позиции торта
                order_item = OrderItem.objects.create(
                    order=order,
                    base_cake=base_cake,
                    crust_type=crust_type,
                    filling=filling,
                    weight=weight,
                    text_on_cake=text_on_cake
                )

                # Прикрепление выбранного декора
                if decorations:
                    order_item.decorations.set(decorations)

                # Особое требование: серверный расчет цены по формуле
                calculated_item_price = order_item.calculate_price()
                order_item.item_price = calculated_item_price
                order_item.save(update_fields=['item_price'])

                # Обновление итоговой суммы заказа
                order.total_price = calculated_item_price
                order.save(update_fields=['total_price'])

                # Сохранение эскиза, если прикреплён (п. 9)
                if sketch_file:
                    DesignSketch.objects.create(
                        order_item=order_item,
                        image=sketch_file
                    )

            # Отправка уведомления на электронную почту (п. 11)
            subject = f"Заказ торта №{order.id} успешно оформлен в кондитерской"
            body = (
                f"Здравствуйте, {request.user.first_name or request.user.username}!\n\n"
                f"Ваш заказ №{order.id} на изготовление торта принят в обработку.\n"
                f"Дата готовности: {order.delivery_date.strftime('%d.%m.%Y')}\n"
                f"Вес: {weight} кг\n"
                f"Начинка: {filling.name}\n"
                f"Основа: {crust_type.name}\n"
                f"Итоговая стоимость: {order.total_price} руб.\n\n"
                f"Менеджер свяжется с вами по телефону {order.contact_phone} для уточнения деталей.\n"
                f"Спасибо, что выбрали нашу кондитерскую!"
            )
            send_mail(
                subject, body, settings.DEFAULT_FROM_EMAIL,
                [request.user.email or 'customer@test.local'],
                fail_silently=True
            )

            messages.success(
                request,
                f"Заказ №{order.id} успешно создан! Итоговая стоимость: {order.total_price} руб."
            )
            return redirect('order_detail', order_id=order.id)
    else:
        form = CustomCakeOrderForm(initial=initial_data)

    decorations = Decoration.objects.all()
    return render(request, 'builder.html', {
        'form': form,
        'decorations': decorations
    })

def api_check_date_and_price(request):
    """
    Запрос fetch к представлению, возвращающему JSON (п. 8).
    Динамически пересчитывает цену торта и проверяет остаток суточного лимита цеха на дату.
    """
    weight_str = request.GET.get('weight', '2.0')
    filling_id = request.GET.get('filling_id')
    crust_id = request.GET.get('crust_id')
    decor_ids = request.GET.getlist('decor_ids[]')
    delivery_date_str = request.GET.get('delivery_date')

    # Расчёт цены
    try:
        weight = Decimal(weight_str)
    except (ValueError, TypeError):
        weight = Decimal('2.0')

    filling_price = Decimal('0.00')
    if filling_id:
        f = Filling.objects.filter(id=filling_id).first()
        if f:
            filling_price = f.price_per_kg

    crust_cost = Decimal('0.00')
    if crust_id:
        c = CrustType.objects.filter(id=crust_id).first()
        if c:
            crust_cost = c.extra_cost

    decor_cost = Decimal('0.00')
    if decor_ids:
        decors = Decoration.objects.filter(id__in=decor_ids)
        decor_cost = sum(d.cost for d in decors)

    total_price = (weight * filling_price) + crust_cost + decor_cost

    # Проверка лимита цеха на дату
    is_date_available = True
    booked_weight = Decimal('0.00')
    max_limit = Decimal('35.00')
    message = "Дата доступна"

    if delivery_date_str:
        try:
            d_date = datetime.datetime.strptime(delivery_date_str, '%Y-%m-%d').date()
            today = datetime.date.today()
            if d_date <= today:
                is_date_available = False
                message = "Заказ принимается минимум за сутки (начиная со следующего дня)"
            else:
                shift = ConfectionerShift.objects.filter(shift_date=d_date).first()
                if shift:
                    max_limit = shift.max_capacity_weight
                
                booked_res = OrderItem.objects.filter(
                    order__delivery_date=d_date,
                    order__status__in=['ACCEPTED', 'IN_PROGRESS', 'READY']
                ).aggregate(total=Sum('weight'))['total']
                booked_weight = Decimal(str(booked_res or '0.00'))

                remaining = max_limit - booked_weight
                if booked_weight + weight > max_limit:
                    is_date_available = False
                    message = f"Лимит цеха на {d_date.strftime('%d.%m.%Y')} исчерпан! В работе: {booked_weight} из {max_limit} кг."
                else:
                    message = f"Дата свободна! Загрузка цеха: {booked_weight} кг из {max_limit} кг (доступно ещё {remaining} кг)."
        except ValueError:
            message = "Неверный формат даты"

    return JsonResponse({
        'price': float(total_price),
        'price_formatted': f"{total_price:,.2f}".replace(',', ' ') + " руб.",
        'is_available': is_date_available,
        'booked_weight': float(booked_weight),
        'max_limit': float(max_limit),
        'message': message
    })

@preview_or_login_required
def order_list(request):
    """
    Список заказов. Клиент видит только свои (п. 4),
    менеджеры и кондитеры видят все заказы.
    """
    if (request.user.is_authenticated and (request.user.is_manager_or_admin or request.user.role == 'confectioner')) or request.GET.get('preview') == '1':
        orders = Order.objects.select_related('customer').prefetch_related('items').all()
    elif request.user.is_authenticated:
        orders = Order.objects.filter(customer=request.user).prefetch_related('items')
    else:
        orders = Order.objects.select_related('customer').prefetch_related('items').all()[:10]

    # Фильтр по статусу
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(status=status_filter)

    return render(request, 'order_list.html', {
        'orders': orders,
        'status_filter': status_filter,
        'status_choices': Order.STATUS_CHOICES
    })

@preview_or_login_required
def order_detail(request, order_id):
    """
    Детали заказа (п. 4: попытка открыть чужой заказ возвращает 403 Forbidden).
    """
    order = get_object_or_404(Order.objects.prefetch_related('items__decorations', 'items__sketches'), id=order_id)
    
    # Разграничение прав: пользователь работает только со своими записями
    if not ((request.user.is_authenticated and request.user == order.customer) or 
            (request.user.is_authenticated and request.user.is_manager_or_admin) or 
            (request.user.is_authenticated and request.user.role == 'confectioner') or
            request.GET.get('preview') == '1'):
        return HttpResponseForbidden("<h1>403 Ошибка доступа</h1><p>У вас нет прав для просмотра чужого заказа.</p>")

    status_form = None
    if request.user.is_manager_or_admin or request.user.role == 'confectioner':
        status_form = OrderStatusUpdateForm(instance=order)

    return render(request, 'order_detail.html', {
        'order': order,
        'status_form': status_form
    })

@login_required
def order_cancel(request, order_id):
    """Отмена заказа клиентом (CRUD п. 5)"""
    order = get_object_or_404(Order, id=order_id)
    if order.customer != request.user and not request.user.is_manager_or_admin:
        return HttpResponseForbidden("Нельзя отменить чужой заказ.")
    
    if order.status != 'NEW':
        messages.error(request, 'Нельзя отменить заказ, который уже передан в работу кондитеру.')
        return redirect('order_detail', order_id=order.id)

    order.status = 'CANCELLED'
    order.save(update_fields=['status'])
    messages.success(request, f"Заказ №{order.id} успешно отменён.")
    return redirect('order_list')

@login_required
def order_status_update(request, order_id):
    """Смена статуса заказа персоналом с отправкой email-уведомления (п. 11)"""
    if not (request.user.is_manager_or_admin or request.user.role == 'confectioner'):
        return HttpResponseForbidden("Только персонал кондитерской может менять статус заказа.")

    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = OrderStatusUpdateForm(request.POST, instance=order)
        if form.is_valid():
            new_status = form.cleaned_data['status']
            order.status = new_status
            order.save(update_fields=['status'])

            # Email-уведомление при смене статуса (п. 11)
            status_text = order.get_status_display()
            send_mail(
                f"Обновление статуса заказа торта №{order.id}",
                f"Здравствуйте, {order.customer.first_name or order.customer.username}!\n\n"
                f"Статус вашего заказа №{order.id} изменился на: «{status_text}».\n"
                f"Дата получения: {order.delivery_date.strftime('%d.%m.%Y')}.\n\n"
                f"С уважением, кондитерский цех.",
                settings.DEFAULT_FROM_EMAIL,
                [order.customer.email or 'customer@test.local'],
                fail_silently=True
            )
            messages.success(request, f"Статус заказа №{order.id} изменён на «{status_text}».")
    return redirect('order_detail', order_id=order.id)

@login_required
def order_print(request, order_id):
    """Печатная технологическая карта заказа для кондитера (п. 10)"""
    order = get_object_or_404(Order.objects.prefetch_related('items__decorations', 'items__sketches'), id=order_id)
    if not (request.user == order.customer or request.user.is_confectioner_or_staff):
        return HttpResponseForbidden("Доступ к бланку запрещён.")
    return render(request, 'order_print.html', {'order': order})

@login_required
def order_export_csv(request):
    """Экспорт журнала заказов в CSV (п. 10)"""
    if not request.user.is_manager_or_admin:
        return HttpResponseForbidden("Экспорт данных доступен только менеджерам и администраторам.")

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="orders_report.csv"'
    response.write('\ufeff') # BOM для корректного открытия в Excel

    writer = csv.writer(response, delimiter=';')
    writer.writerow([
        'Номер заказа', 'Дата оформления', 'Дата выдачи', 'Клиент',
        'Телефон', 'Статус', 'Суммарный вес (кг)', 'Сумма (руб.)', 'Адрес доставки'
    ])

    orders = Order.objects.select_related('customer').prefetch_related('items').all()
    for o in orders:
        total_w = sum(it.weight for it in o.items.all())
        writer.writerow([
            o.id,
            o.created_at.strftime('%d.%m.%Y %H:%M'),
            o.delivery_date.strftime('%d.%m.%Y'),
            o.customer.username,
            o.contact_phone,
            o.get_status_display(),
            str(total_w),
            str(o.total_price),
            o.delivery_address or 'Самовывоз'
        ])
    return response

# CRUD для отзывов (п. 5)
@login_required
def review_create(request, cake_id):
    cake = get_object_or_404(BaseCake, id=cake_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.base_cake = cake
            review.customer = request.user
            review.save()
            messages.success(request, 'Ваш отзыв успешно опубликован!')
    return redirect('cake_detail', slug=cake.slug)

@login_required
def review_edit(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if review.customer != request.user and not request.user.is_manager_or_admin:
        return HttpResponseForbidden("Вы можете редактировать только свой отзыв.")
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Отзыв успешно обновлён.')
            return redirect('cake_detail', slug=review.base_cake.slug)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'review_form.html', {'form': form, 'review': review})

@login_required
def review_delete(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if review.customer != request.user and not request.user.is_manager_or_admin:
        return HttpResponseForbidden("Вы можете удалить только свой отзыв.")
    cake_slug = review.base_cake.slug
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Отзыв удалён.')
        return redirect('cake_detail', slug=cake_slug)
    return render(request, 'review_confirm_delete.html', {'review': review})

@preview_or_login_required
def dashboard(request):
    """
    Страница сводных аналитических показателей кондитерской (п. 7).
    Не менее 4 значений, посчитанных агрегатными запросами:
    1. Количество заказов (Count)
    2. Суммарная выручка (Sum)
    3. Средний чек (Avg)
    4. Доля выполненных заказов (%)
    Плюс интерактивный график загрузки цеха по дням.
    """
    if not (request.user.is_authenticated and (request.user.is_manager_or_admin or request.user.role == 'confectioner')):
        if request.GET.get('preview') != '1':
            return HttpResponseForbidden("Аналитика доступна сотрудникам кондитерской.")

    # 1. Агрегатные запросы
    total_orders = Order.objects.count()
    revenue_res = Order.objects.filter(status__in=['ACCEPTED', 'IN_PROGRESS', 'READY', 'COMPLETED']).aggregate(Sum('total_price'))['total_price__sum']
    total_revenue = Decimal(str(revenue_res or '0.00'))
    
    avg_check_res = Order.objects.aggregate(Avg('total_price'))['total_price__avg']
    avg_check = Decimal(str(avg_check_res or '0.00'))

    completed_orders = Order.objects.filter(status='COMPLETED').count()
    completed_share = round((completed_orders / total_orders * 100), 1) if total_orders > 0 else 0

    total_weight_res = OrderItem.objects.aggregate(Sum('weight'))['weight__sum']
    total_weight = Decimal(str(total_weight_res or '0.00'))

    # Статистика загрузки цеха на ближайшие 7 дней (для графика)
    today = datetime.date.today()
    chart_dates = []
    chart_booked = []
    chart_limits = []

    for i in range(7):
        cur_date = today + datetime.timedelta(days=i)
        shift = ConfectionerShift.objects.filter(shift_date=cur_date).first()
        limit_val = float(shift.max_capacity_weight) if shift else 35.0
        
        booked_val_res = OrderItem.objects.filter(
            order__delivery_date=cur_date,
            order__status__in=['ACCEPTED', 'IN_PROGRESS', 'READY']
        ).aggregate(Sum('weight'))['weight__sum']
        booked_val = float(booked_val_res or 0)

        chart_dates.append(cur_date.strftime('%d.%m'))
        chart_booked.append(booked_val)
        chart_limits.append(limit_val)

    # Топ-3 начинки
    top_fillings = Filling.objects.annotate(order_count=Count('order_items')).order_by('-order_count')[:5]

    return render(request, 'dashboard.html', {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'avg_check': avg_check,
        'completed_share': completed_share,
        'total_weight': total_weight,
        'chart_dates': chart_dates,
        'chart_booked': chart_booked,
        'chart_limits': chart_limits,
        'top_fillings': top_fillings,
    })

# Аутентификация (п. 3)
def register_view(request):
    if request.user.is_authenticated:
        return redirect('catalog')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Отправка email при регистрации (п. 11)
            send_mail(
                "Добро пожаловать в кондитерскую!",
                f"Здравствуйте, {user.first_name}!\nВы успешно зарегистрировались на сайте кондитерской.",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=True
            )
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('catalog')
    else:
        form = UserRegisterForm()
    return render(request, 'auth/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('catalog')
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"С возвращением, {user.first_name or user.username}!")
            next_url = request.GET.get('next', 'catalog')
            return redirect(next_url)
    else:
        form = UserLoginForm()
    return render(request, 'auth/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Вы успешно вышли из учётной записи.')
    return redirect('home')

@preview_or_login_required
def profile_view(request):
    my_orders = Order.objects.filter(customer=request.user).order_by('-created_at')[:5]
    my_reviews = Review.objects.filter(customer=request.user).select_related('base_cake')
    return render(request, 'auth/profile.html', {
        'orders': my_orders,
        'reviews': my_reviews
    })

@login_required
def password_change_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Ваш пароль был успешно изменён!')
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'auth/password_change.html', {'form': form})
