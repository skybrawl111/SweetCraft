from django.urls import path
from . import views

urlpatterns = [
    # Главная и каталог (п. 6)
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('cakes/<slug:slug>/', views.cake_detail, name='cake_detail'),

    # Интерактивный конструктор заказа торта (п. 1, Особое требование)
    path('builder/', views.cake_builder, name='cake_builder'),
    
    # API JSON fetch для асинхронного пересчета цены и проверки лимита цеха (п. 8)
    path('api/check-date-and-price/', views.api_check_date_and_price, name='api_check_date_and_price'),

    # Заказы (CRUD на сайте п. 5, печать и CSV п. 10)
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/<int:order_id>/cancel/', views.order_cancel, name='order_cancel'),
    path('orders/<int:order_id>/status/', views.order_status_update, name='order_status_update'),
    path('orders/<int:order_id>/print/', views.order_print, name='order_print'),
    path('orders/export-csv/', views.order_export_csv, name='order_export_csv'),

    # Отзывы (CRUD на сайте п. 5)
    path('cakes/<int:cake_id>/review/add/', views.review_create, name='review_create'),
    path('reviews/<int:review_id>/edit/', views.review_edit, name='review_edit'),
    path('reviews/<int:review_id>/delete/', views.review_delete, name='review_delete'),

    # Сводная панель аналитики с графиком (п. 7)
    path('dashboard/', views.dashboard, name='dashboard'),

    # Аутентификация и профиль (п. 3)
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/password-change/', views.password_change_view, name='password_change'),
]
