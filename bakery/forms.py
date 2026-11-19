from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Sum
from decimal import Decimal
import datetime

from .models import (
    CustomUser, BaseCake, CrustType, Filling, Decoration,
    Order, OrderItem, DesignSketch, Review, ConfectionerShift
)

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True, label='Имя')
    last_name = forms.CharField(max_length=50, required=False, label='Фамилия')
    email = forms.EmailField(required=True, label='Адрес электронной почты')
    phone = forms.CharField(max_length=25, required=True, label='Номер телефона')

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'phone')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже зарегистрирован.')
        return email

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваш логин'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))

class CustomCakeOrderForm(forms.Form):
    """
    Форма интерактивного конструктора торта и оформления заказа.
    Реализует валидацию особого требования Варианта 1:
    - Проверка суточного лимита веса цеха на выбранную дату;
    - Валидация загружаемого эскиза (тип и размер до 5 МБ, п. 9).
    """
    base_cake = forms.ModelChoiceField(
        queryset=BaseCake.objects.filter(is_available=True),
        required=False,
        label='Базовый торт (если выбираете из каталога)',
        empty_label='— Свой индивидуальный торт —',
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_base_cake'})
    )
    crust_type = forms.ModelChoiceField(
        queryset=CrustType.objects.all(),
        required=True,
        label='Вид основы (бисквит / корж)',
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_crust_type'})
    )
    filling = forms.ModelChoiceField(
        queryset=Filling.objects.filter(is_active=True),
        required=True,
        label='Начинка',
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_filling'})
    )
    weight = forms.DecimalField(
        max_digits=4,
        decimal_places=2,
        min_value=Decimal('1.00'),
        max_value=Decimal('20.00'),
        initial=Decimal('2.00'),
        label='Вес торта (кг)',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5', 'id': 'id_weight'})
    )
    decorations = forms.ModelMultipleChoiceField(
        queryset=Decoration.objects.all(),
        required=False,
        label='Элементы сложного декора',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'decor-checkbox'})
    )
    text_on_cake = forms.CharField(
        max_length=150,
        required=False,
        label='Поздравительная надпись на торте',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: С Днем Рождения, Анна!'})
    )
    delivery_date = forms.DateField(
        required=True,
        label='Желаемая дата готовности / выдачи',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'id': 'id_delivery_date'})
    )
    contact_phone = forms.CharField(
        max_length=25,
        required=True,
        label='Контактный телефон для связи',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (999) 000-00-00'})
    )
    delivery_address = forms.CharField(
        max_length=250,
        required=False,
        label='Адрес доставки (оставьте пустым для самовывоза)',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'г. Москва, ул. Ленина, д. 10 (или самовывоз из цеха)'})
    )
    comment = forms.CharField(
        required=False,
        label='Дополнительные пожелания к рецептуре и оформлению',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Аллергия на орехи, форма торта, цвет велюра...'})
    )
    sketch_image = forms.FileField(
        required=False,
        label='Загрузить эскиз / фото желаемого оформления (JPG, PNG, до 5 МБ)',
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/jpeg,image/png,image/webp'})
    )

    def clean_delivery_date(self):
        delivery_date = self.cleaned_data.get('delivery_date')
        if not delivery_date:
            return delivery_date
        
        today = timezone.localdate()
        if delivery_date <= today:
            raise ValidationError('Заказ заказных десертов принимается минимум за 24 часа (начиная с завтрашнего дня).')
        return delivery_date

    def clean_sketch_image(self):
        sketch = self.cleaned_data.get('sketch_image')
        if sketch:
            # Проверка размера файла (не более 5 МБ)
            if sketch.size > 5 * 1024 * 1024:
                raise ValidationError('Размер загружаемого файла эскиза не должен превышать 5 МБ.')
            # Проверка расширения файла
            ext = sketch.name.split('.')[-1].lower()
            if ext not in ['jpg', 'jpeg', 'png', 'webp']:
                raise ValidationError('Допустимы только файлы изображений формата JPG, PNG, WEBP.')
        return sketch

    def clean(self):
        cleaned_data = super().clean()
        delivery_date = cleaned_data.get('delivery_date')
        weight = cleaned_data.get('weight')

        if delivery_date and weight:
            # ОСОБОЕ ТРЕБОВАНИЕ ВАРИАНТА 1:
            # Проверка суточного лимита веса цеха на выбранную дату
            shift = ConfectionerShift.objects.filter(shift_date=delivery_date).first()
            max_limit = shift.max_capacity_weight if shift else Decimal('35.00')
            
            booked_weight_res = OrderItem.objects.filter(
                order__delivery_date=delivery_date,
                order__status__in=['ACCEPTED', 'IN_PROGRESS', 'READY']
            ).aggregate(total=Sum('weight'))['total']
            
            booked_weight = Decimal(str(booked_weight_res or '0.00'))
            new_total = booked_weight + Decimal(str(weight))

            if new_total > max_limit:
                rem = max(Decimal('0.00'), max_limit - booked_weight)
                err_msg = (
                    f"На дату {delivery_date.strftime('%d.%m.%Y')} суточный лимит кондитерского цеха исчерпан! "
                    f"Уже в работе: {booked_weight} кг из {max_limit} кг (осталось свободно: {rem} кг). "
                    f"Пожалуйста, выберите другую дату или уменьшите вес заказа."
                )
                self.add_error('delivery_date', err_msg)
                raise ValidationError(err_msg)

        return cleaned_data

class OrderStatusUpdateForm(forms.ModelForm):
    """Форма смены статуса заказа для менеджера и кондитера"""
    class Meta:
        model = Order
        fields = ('status',)
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

class ReviewForm(forms.ModelForm):
    """Форма добавления и редактирования отзыва (CRUD на сайте, п. 5)"""
    class Meta:
        model = Review
        fields = ('rating', 'text')
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Поделитесь впечатлениями о вкусе, бисквите и оформлении...'}),
        }
