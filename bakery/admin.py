from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser, Category, CrustType, Filling, Decoration,
    BaseCake, ConfectionerShift, Order, OrderItem, OrderItemDecoration,
    DesignSketch, Review
)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'phone', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Роль и контакты в кондитерской', {'fields': ('role', 'phone')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Роль и контакты в кондитерской', {'fields': ('role', 'phone')}),
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(CrustType)
class CrustTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'extra_cost')
    search_fields = ('name',)

@admin.register(Filling)
class FillingAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_per_kg', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)

@admin.register(Decoration)
class DecorationAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost')
    search_fields = ('name',)

@admin.register(BaseCake)
class BaseCakeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'base_price', 'default_weight', 'crust_type', 'is_available', 'created_at')
    list_filter = ('category', 'is_available', 'crust_type')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('available_fillings',)

@admin.register(ConfectionerShift)
class ConfectionerShiftAdmin(admin.ModelAdmin):
    list_display = ('shift_date', 'confectioner', 'max_capacity_weight', 'get_booked_weight_display', 'get_remaining_weight_display')
    list_filter = ('shift_date', 'confectioner')
    ordering = ('-shift_date',)

    def get_booked_weight_display(self, obj):
        return f"{obj.get_booked_weight()} кг"
    get_booked_weight_display.short_description = 'Вес в работе'

    def get_remaining_weight_display(self, obj):
        return f"{obj.get_remaining_weight()} кг"
    get_remaining_weight_display.short_description = 'Свободно'

class OrderItemDecorationInline(admin.TabularInline):
    model = OrderItemDecoration
    extra = 1

class DesignSketchInline(admin.TabularInline):
    model = DesignSketch
    extra = 0

class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'delivery_date', 'status', 'total_price', 'contact_phone', 'created_at')
    list_filter = ('status', 'delivery_date', 'created_at')
    search_fields = ('id', 'customer__username', 'contact_phone', 'delivery_address')
    inlines = [OrderItemInline]
    actions = ['mark_accepted', 'mark_in_progress', 'mark_ready', 'mark_completed']

    def mark_accepted(self, request, queryset):
        queryset.update(status='ACCEPTED')
    mark_accepted.short_description = 'Перевести в статус: Принят в работу'

    def mark_in_progress(self, request, queryset):
        queryset.update(status='IN_PROGRESS')
    mark_in_progress.short_description = 'Перевести в статус: В работе (выпекается)'

    def mark_ready(self, request, queryset):
        queryset.update(status='READY')
    mark_ready.short_description = 'Перевести в статус: Готов к выдаче'

    def mark_completed(self, request, queryset):
        queryset.update(status='COMPLETED')
    mark_completed.short_description = 'Перевести в статус: Выдан клиенту'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'base_cake', 'crust_type', 'filling', 'tiers', 'weight', 'item_price')
    list_filter = ('crust_type', 'filling', 'tiers')
    search_fields = ('order__id', 'text_on_cake')
    inlines = [OrderItemDecorationInline, DesignSketchInline]

@admin.register(OrderItemDecoration)
class OrderItemDecorationAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_item', 'decoration', 'quantity', 'custom_notes')
    list_filter = ('decoration',)
    search_fields = ('order_item__id', 'decoration__name')

@admin.register(DesignSketch)
class DesignSketchAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_item', 'uploaded_at')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('base_cake', 'customer', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('base_cake__title', 'customer__username', 'text')

admin.site.site_header = "SweetCraft: Панель администрирования"
admin.site.site_title = "SweetCraft Администрирование"
admin.site.index_title = "Управление кондитерской SweetCraft"

