from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.db.models import Sum, Q, F
from decimal import Decimal

class CustomUser(AbstractUser):
    """Пользователь системы с разделением ролей"""
    ROLE_CHOICES = (
        ('customer', 'Покупатель'),
        ('confectioner', 'Кондитер цеха'),
        ('manager', 'Менеджер заказов'),
        ('admin', 'Администратор'),
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='customer',
        verbose_name='Роль пользователя'
    )
    phone = models.CharField(
        max_length=25,
        blank=True,
        verbose_name='Контактный телефон'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']

    def __str__(self):
        full_name = self.get_full_name()
        return f"{self.username} ({full_name or self.get_role_display()})"

    @property
    def is_manager_or_admin(self):
        return self.role in ('manager', 'admin') or self.is_superuser

    @property
    def is_confectioner_or_staff(self):
        return self.role in ('confectioner', 'manager', 'admin') or self.is_staff

class Category(models.Model):
    """Категория кондитерских изделий (торты, капкейки, бенто, десерты)"""
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='URL-слаг'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание категории'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Отображать в каталоге'
    )

    class Meta:
        verbose_name = 'Категория десертов'
        verbose_name_plural = 'Категории десертов'
        ordering = ['name']

    def __str__(self):
        return self.name

class CrustType(models.Model):
    """Вид коржа (бисквита)"""
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название коржа'
    )
    extra_cost = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name='Базовая стоимость коржа (руб.)'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание вкуса и текстуры'
    )

    class Meta:
        verbose_name = 'Вид коржа'
        verbose_name_plural = 'Виды коржей'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} (+{self.extra_cost} руб.)" if self.extra_cost else self.name

class Filling(models.Model):
    """Начинка торта"""
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название начинки'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание состава'
    )
    price_per_kg = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='Стоимость начинки за 1 кг (руб.)'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Доступна для заказа'
    )

    class Meta:
        verbose_name = 'Начинка'
        verbose_name_plural = 'Начинки'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.price_per_kg} руб./кг)"

class Decoration(models.Model):
    """Элемент оформления / декор"""
    name = models.CharField(
        max_length=120,
        unique=True,
        verbose_name='Название декора'
    )
    cost = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name='Надбавка за декор (руб.)'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание декора'
    )

    class Meta:
        verbose_name = 'Элемент декора'
        verbose_name_plural = 'Элементы декора'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} (+{self.cost} руб.)"

class BaseCake(models.Model):
    """Каталожный базовый торт / десерт"""
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cakes',
        verbose_name='Категория десерта'
    )
    title = models.CharField(
        max_length=150,
        verbose_name='Название торта'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='URL-метка'
    )
    description = models.TextField(
        verbose_name='Подробное описание'
    )
    base_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='Базовая цена (руб.)'
    )
    default_weight = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=Decimal('2.00'),
        verbose_name='Стандартный вес (кг)'
    )
    crust_type = models.ForeignKey(
        CrustType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='base_cakes',
        verbose_name='Рекомендуемый корж'
    )
    available_fillings = models.ManyToManyField(
        Filling,
        blank=True,
        related_name='base_cakes',
        verbose_name='Совместимые начинки'
    )
    image = models.ImageField(
        upload_to='cakes/',
        blank=True,
        null=True,
        verbose_name='Фотография торта'
    )
    is_available = models.BooleanField(
        default=True,
        verbose_name='Доступен в каталоге'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
    )

    class Meta:
        verbose_name = 'Базовый торт'
        verbose_name_plural = 'Базовые торты'
        ordering = ['-created_at']

    def __str__(self):
        cat = f"[{self.category.name}] " if self.category else ""
        return f"{cat}{self.title} — от {self.base_price} руб."

class ConfectionerShift(models.Model):
    """Смена кондитера и суточный лимит цеха (Особое требование Варианта 1)"""
    shift_date = models.DateField(
        verbose_name='Дата смены'
    )
    confectioner = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role__in': ['confectioner', 'admin', 'manager']},
        related_name='shifts',
        verbose_name='Дежурный кондитер'
    )
    max_capacity_weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('35.00'),
        verbose_name='Суточный лимит цеха (кг)'
    )
    notes = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Заметки к смене'
    )

    class Meta:
        verbose_name = 'Смена кондитера и лимит цеха'
        verbose_name_plural = 'Смены кондитеров и лимиты цеха'
        ordering = ['shift_date']
        constraints = [
            models.UniqueConstraint(
                fields=['shift_date', 'confectioner'],
                name='unique_confectioner_shift_per_day'
            ),
            models.CheckConstraint(
                check=models.Q(max_capacity_weight__gte=Decimal('10.00')),
                name='check_shift_min_capacity_10kg'
            )
        ]

    def __str__(self):
        return f"Смена {self.shift_date}: лимит {self.max_capacity_weight} кг (Кондитер: {self.confectioner or 'Цех'})"

    def get_booked_weight(self):
        """Суммарный вес активных тортов в работе на эту дату"""
        res = OrderItem.objects.filter(
            order__delivery_date=self.shift_date,
            order__status__in=['ACCEPTED', 'IN_PROGRESS', 'READY']
        ).aggregate(total=Sum('weight'))['total']
        return Decimal(str(res or '0.00'))

    def get_remaining_weight(self):
        """Остаток доступного веса на смену"""
        rem = self.max_capacity_weight - self.get_booked_weight()
        return max(Decimal('0.00'), rem)

class Order(models.Model):
    """Заказ покупателя"""
    STATUS_CHOICES = (
        ('NEW', 'Новый (на рассмотрении)'),
        ('ACCEPTED', 'Принят в работу'),
        ('IN_PROGRESS', 'Выпекается и декорируется'),
        ('READY', 'Готов к выдаче'),
        ('COMPLETED', 'Выдан клиенту'),
        ('CANCELLED', 'Отменён'),
    )

    customer = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Покупатель'
    )
    delivery_date = models.DateField(
        verbose_name='Желаемая дата выдачи'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='NEW',
        verbose_name='Статус заказа'
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name='Итоговая цена (руб.)'
    )
    contact_phone = models.CharField(
        max_length=25,
        verbose_name='Контактный телефон'
    )
    delivery_address = models.CharField(
        max_length=250,
        blank=True,
        verbose_name='Адрес доставки (или самовывоз)'
    )
    comment = models.TextField(
        blank=True,
        verbose_name='Пожелания и комментарии'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата оформления'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']
        constraints = [
            models.CheckConstraint(
                check=models.Q(total_price__gte=Decimal('0.00')),
                name='check_order_total_price_non_negative'
            )
        ]

    def __str__(self):
        return f"Заказ №{self.id} от {self.delivery_date} ({self.get_status_display()}) — {self.total_price} руб."

    def recalculate_total(self):
        """Пересчёт суммарной цены заказа из всех его позиций"""
        total = sum(item.item_price for item in self.items.all())
        self.total_price = total
        self.save(update_fields=['total_price'])

class OrderItem(models.Model):
    """Позиция заказа (индивидуально собранный торт)"""
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Заказ'
    )
    base_cake = models.ForeignKey(
        BaseCake,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='order_items',
        verbose_name='Базовая основа'
    )
    crust_type = models.ForeignKey(
        CrustType,
        on_delete=models.PROTECT,
        related_name='order_items',
        verbose_name='Корж'
    )
    filling = models.ForeignKey(
        Filling,
        on_delete=models.PROTECT,
        related_name='order_items',
        verbose_name='Начинка'
    )
    tiers = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(3)],
        verbose_name='Количество ярусов'
    )
    weight = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('1.00')), MaxValueValidator(Decimal('20.00'))],
        verbose_name='Вес торта (кг)'
    )
    item_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name='Стоимость торта (руб.)'
    )
    text_on_cake = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Надпись на торте'
    )
    decorations = models.ManyToManyField(
        Decoration,
        through='OrderItemDecoration',
        blank=True,
        related_name='order_items',
        verbose_name='Элементы декора'
    )

    class Meta:
        verbose_name = 'Позиция заказа (торт)'
        verbose_name_plural = 'Позиции заказа (торты)'
        ordering = ['id']
        constraints = [
            models.CheckConstraint(
                check=models.Q(weight__gte=Decimal('1.00')) & models.Q(weight__lte=Decimal('20.00')),
                name='check_orderitem_weight_range'
            ),
            models.CheckConstraint(
                check=models.Q(tiers__gte=1) & models.Q(tiers__lte=3),
                name='check_orderitem_tiers_1_to_3'
            )
        ]

    def __str__(self):
        return f"Торт {self.weight} кг, {self.tiers} яр. ({self.crust_type.name}, {self.filling.name}) — {self.item_price} руб."

    def calculate_price(self):
        """
        Особое требование Варианта 1:
        Формула: Price = (Weight * Filling_price) + Crust_cost + SUM(Decorations_cost)
        """
        weight_decimal = Decimal(str(self.weight))
        filling_price = Decimal(str(self.filling.price_per_kg)) if self.filling else Decimal('0.00')
        crust_cost = Decimal(str(self.crust_type.extra_cost)) if self.crust_type else Decimal('0.00')
        
        decor_cost = Decimal('0.00')
        if self.pk:
            for d in self.decorations.all():
                decor_cost += Decimal(str(d.cost))

        total = (weight_decimal * filling_price) + crust_cost + decor_cost
        return total

class OrderItemDecoration(models.Model):
    """Связующая таблица декора позиции заказа (M:M с собственными атрибутами)"""
    order_item = models.ForeignKey(
        OrderItem,
        on_delete=models.CASCADE,
        related_name='item_decorations',
        verbose_name='Позиция заказа'
    )
    decoration = models.ForeignKey(
        Decoration,
        on_delete=models.PROTECT,
        related_name='item_decorations',
        verbose_name='Элемент декора'
    )
    quantity = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(50)],
        verbose_name='Количество элементов'
    )
    custom_notes = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Пожелания по размещению декора'
    )

    class Meta:
        verbose_name = 'Декор позиции заказа'
        verbose_name_plural = 'Декоры позиций заказа'
        constraints = [
            models.UniqueConstraint(
                fields=['order_item', 'decoration'],
                name='unique_decoration_per_order_item'
            ),
            models.CheckConstraint(
                check=models.Q(quantity__gte=1) & models.Q(quantity__lte=50),
                name='check_decoration_quantity_range'
            )
        ]

    def __str__(self):
        return f"{self.decoration.name} x{self.quantity} для поз. #{self.order_item_id}"

class DesignSketch(models.Model):
    """Загруженный покупателем эскиз или пример оформления"""
    order_item = models.ForeignKey(
        OrderItem,
        on_delete=models.CASCADE,
        related_name='sketches',
        verbose_name='Позиция заказа'
    )
    image = models.ImageField(
        upload_to='sketches/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])],
        verbose_name='Файл эскиза'
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата загрузки'
    )

    class Meta:
        verbose_name = 'Эскиз оформления'
        verbose_name_plural = 'Эскизы оформления'
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"Эскиз к позиции #{self.order_item_id}"

class Review(models.Model):
    """Отзыв покупателя о торте (CRUD на сайте)"""
    RATING_CHOICES = (
        (5, '★★★★★ — Отлично'),
        (4, '★★★★☆ — Хорошо'),
        (3, '★★★☆☆ — Удовлетворительно'),
        (2, '★★☆☆☆ — Плохо'),
        (1, '★☆☆☆☆ — Ужасно'),
    )
    base_cake = models.ForeignKey(
        BaseCake,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Торт'
    )
    customer = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Покупатель'
    )
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        default=5,
        verbose_name='Оценка'
    )
    text = models.TextField(
        verbose_name='Текст отзыва'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата отзыва'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']
        constraints = [
            models.CheckConstraint(
                check=models.Q(rating__gte=1) & models.Q(rating__lte=5),
                name='check_review_rating_1_to_5'
            )
        ]

    def __str__(self):
        return f"Отзыв от {self.customer.username} на {self.base_cake.title} ({self.rating}★)"
