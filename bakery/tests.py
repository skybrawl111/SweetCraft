from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from decimal import Decimal
import datetime

from bakery.models import (
    CustomUser, CrustType, Filling, Decoration,
    BaseCake, ConfectionerShift, Order, OrderItem, Review
)

class BakerySystemTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Создание пользователей
        self.admin = CustomUser.objects.create_superuser(
            username='admin_test', email='admin@test.local', password='password123', role='admin'
        )
        self.manager = CustomUser.objects.create_user(
            username='manager_test', email='manager@test.local', password='password123', role='manager'
        )
        self.customer1 = CustomUser.objects.create_user(
            username='user1', email='user1@test.local', password='password123', role='customer'
        )
        self.customer2 = CustomUser.objects.create_user(
            username='user2', email='user2@test.local', password='password123', role='customer'
        )

        # Справочники
        self.crust = CrustType.objects.create(name='Шоколадный', extra_cost=Decimal('500.00'))
        self.filling = Filling.objects.create(name='Малина-мята', price_per_kg=Decimal('1200.00'))
        self.decor1 = Decoration.objects.create(name='Ягоды', cost=Decimal('800.00'))
        self.decor2 = Decoration.objects.create(name='Велюр', cost=Decimal('700.00'))

        self.cake = BaseCake.objects.create(
            title='Тестовый торт',
            slug='test-cake',
            description='Вкусный торт',
            base_price=Decimal('2500.00'),
            default_weight=Decimal('2.0'),
            crust_type=self.crust
        )

    def test_special_requirement_price_formula(self):
        """
        Проверка формулы особого требования Варианта 1:
        Price = (Weight * Filling_price) + Crust_cost + SUM(Decorations)
        Пример: вес 3 кг * 1200 руб + 500 руб (корж) + 800 руб (декор 1) + 700 руб (декор 2)
        = 3600 + 500 + 1500 = 5600 руб.
        """
        order = Order.objects.create(
            customer=self.customer1,
            delivery_date=timezone.localdate() + datetime.timedelta(days=3),
            status='NEW'
        )
        item = OrderItem.objects.create(
            order=order,
            base_cake=self.cake,
            crust_type=self.crust,
            filling=self.filling,
            weight=Decimal('3.00')
        )
        item.decorations.set([self.decor1, self.decor2])
        calculated_price = item.calculate_price()
        self.assertEqual(calculated_price, Decimal('5600.00'))

    def test_special_requirement_workshop_capacity_limit(self):
        """
        Проверка особого требования: блокировка заказа, если суммарный вес
        в работе на дату уже превысил суточный лимит цеха (например 35 кг).
        """
        test_date = timezone.localdate() + datetime.timedelta(days=2)
        ConfectionerShift.objects.create(
            shift_date=test_date,
            max_capacity_weight=Decimal('30.00')
        )

        # Создаём существующий заказ в работе на 28 кг (два изделия по 14 кг в пределах ограничения 1..20 кг)
        existing_order = Order.objects.create(
            customer=self.customer2,
            delivery_date=test_date,
            status='ACCEPTED'
        )
        OrderItem.objects.create(
            order=existing_order,
            crust_type=self.crust,
            filling=self.filling,
            weight=Decimal('14.00'),
            item_price=Decimal('5000.00')
        )
        OrderItem.objects.create(
            order=existing_order,
            crust_type=self.crust,
            filling=self.filling,
            weight=Decimal('14.00'),
            item_price=Decimal('5000.00')
        )

        # Пытаемся заказать торт весом 4 кг (28 + 4 = 32 > 30 лимита цеха)
        self.client.login(username='user1', password='password123')
        response = self.client.post(reverse('cake_builder'), {
            'crust_type': self.crust.id,
            'filling': self.filling.id,
            'weight': '4.0',
            'delivery_date': test_date.strftime('%Y-%m-%d'),
            'contact_phone': '+79991112233'
        })

        # Должна вернуться ошибка формы о превышении лимита цеха
        self.assertContains(response, 'суточный лимит кондитерского цеха исчерпан')

    def test_access_control_403_on_foreign_order(self):
        """
        Проверка требования 4: пользователь видит только свои записи.
        Попытка открыть чужой заказ возвращает 403 Forbidden.
        """
        order_user1 = Order.objects.create(
            customer=self.customer1,
            delivery_date=timezone.localdate() + datetime.timedelta(days=3),
            status='NEW'
        )

        # Входим как user2 и пытаемся открыть заказ user1
        self.client.login(username='user2', password='password123')
        response = self.client.get(reverse('order_detail', args=[order_user1.id]))
        self.assertEqual(response.status_code, 403)

    def test_fetch_json_api_response(self):
        """
        Проверка требования 8: запрос fetch возвращает JSON с пересчитанной ценой
        и статусом доступности суточного лимита.
        """
        test_date = timezone.localdate() + datetime.timedelta(days=5)
        response = self.client.get(reverse('api_check_date_and_price'), {
            'weight': '2.5',
            'filling_id': self.filling.id,
            'crust_id': self.crust.id,
            'delivery_date': test_date.strftime('%Y-%m-%d'),
            'decor_ids[]': [self.decor1.id]
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # Price = 2.5 * 1200 + 500 + 800 = 3000 + 1300 = 4300
        self.assertEqual(data['price'], 4300.0)
        self.assertTrue(data['is_available'])

    def test_catalog_search_and_pagination(self):
        """
        Проверка требования 6: каталог десертов с поиском и фильтрацией.
        """
        response = self.client.get(reverse('catalog'), {'q': 'Тестовый'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Тестовый торт')
