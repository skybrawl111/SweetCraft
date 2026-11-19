# -*- coding: utf-8 -*-
"""
Выполнение 5 аналитических запросов ORM и SQL к базе данных для Занятия 5.
Выводит ORM-код, сгенерированный SQL (через str(qs.query)) и результат выполнения.
Сохраняет отчет в файл queries_day5.txt.
"""

import os
import sys
from pathlib import Path

# Корень проекта (3 уровня вверх от scripts/tools/run_queries_day5.py)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
os.chdir(BASE_DIR)

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'confectionery_project.settings')
django.setup()

from decimal import Decimal
from django.db.models import Count, Avg, Sum, Max, Min, Q
from django.db import connection, reset_queries
from bakery.models import (
    CustomUser, Category, CrustType, Filling, Decoration,
    BaseCake, ConfectionerShift, Order, OrderItem, OrderItemDecoration, Review
)

def run_all_queries():
    output_lines = []
    
    def log(text=""):
        print(text)
        output_lines.append(text)

    log("=" * 80)
    log("ПРАКТИЧЕСКОЕ ЗАНЯТИЕ № 5. АНАЛИТИЧЕСКИЕ ЗАПРОСЫ К БАЗЕ ДАННЫХ (ORM & SQL)")
    log("Проект: Веб-сервис приема заказов кондитерской «SweetCraft» (Вариант 1)")
    log("Студент: Адилов Чошгун, группа ИСП-41")
    log("=" * 80)
    log()

    # -------------------------------------------------------------
    # ЗАПРОС 1: Фильтрация по условию
    # -------------------------------------------------------------
    log("-" * 80)
    log("ЗАПРОС 1: ФИЛЬТРАЦИЯ ПО УСЛОВИЮ (Доступные начинки в ценовом диапазоне)")
    log("-" * 80)
    log("Бизнес-задача: Выбрать все активные начинки для онлайн-конструктора со стоимостью от 1200 до 1500 руб./кг.")
    log()
    log("[ORM-запрос]:")
    log("qs1 = Filling.objects.filter(")
    log("    is_active=True,")
    log("    price_per_kg__gte=Decimal('1200.00'),")
    log("    price_per_kg__lte=Decimal('1500.00')")
    log(").order_by('price_per_kg')")
    log()
    
    qs1 = Filling.objects.filter(
        is_active=True,
        price_per_kg__gte=Decimal('1200.00'),
        price_per_kg__lte=Decimal('1500.00')
    ).order_by('price_per_kg')
    
    log("[Сгенерированный SQL (через str(queryset.query))]:")
    log(str(qs1.query))
    log()
    log("[Результат выполнения (найдено записей: %d)]:" % qs1.count())
    log(f"{'ID':<4} | {'Название начинки':<45} | {'Цена за 1 кг':<12} | {'Статус':<8}")
    log("-" * 75)
    for f in qs1:
        status_str = "Активна" if f.is_active else "Отключена"
        log(f"{f.id:<4} | {f.name:<45} | {f.price_per_kg:>8} руб. | {status_str:<8}")
    log()

    # -------------------------------------------------------------
    # ЗАПРОС 2: Сортировка по нескольким полям
    # -------------------------------------------------------------
    log("-" * 80)
    log("ЗАПРОС 2: СОРТИРОВКА ПО НЕСКОЛЬКИМ ПОЛЯМ (Каталог тортов по цене и названию)")
    log("-" * 80)
    log("Бизнес-задача: Выгрузить десерты каталога, отсортированные по возрастанию базовой цены, а при одинаковой цене — по алфавиту названия.")
    log()
    log("[ORM-запрос]:")
    log("qs2 = BaseCake.objects.filter(is_available=True).order_by('base_price', 'title')[:8]")
    log()
    
    qs2 = BaseCake.objects.filter(is_available=True).order_by('base_price', 'title')[:8]
    log("[Сгенерированный SQL (через str(queryset.query))]:")
    log(str(qs2.query))
    log()
    log("[Результат выполнения (первые 8 позиций)]:")
    log(f"{'ID':<4} | {'Название торта/десерта':<45} | {'Базовая цена':<14} | {'Вес по умолч.':<12}")
    log("-" * 80)
    for b in qs2:
        log(f"{b.id:<4} | {b.title:<45} | {b.base_price:>9} руб. | {b.default_weight:>7} кг")
    log()

    # -------------------------------------------------------------
    # ЗАПРОС 3: Агрегация данных (Count, Sum, Avg, Max)
    # -------------------------------------------------------------
    log("-" * 80)
    log("ЗАПРОС 3: АГРЕГАЦИЯ ДАННЫХ (Расчет финансово-производственных показателей)")
    log("-" * 80)
    log("Бизнес-задача: Посчитать сводную статистику по подтвержденным заказам: количество, суммарную выручку, средний чек и максимальную стоимость заказа.")
    log()
    log("[ORM-запрос]:")
    log("qs3 = Order.objects.filter(")
    log("    status__in=['ACCEPTED', 'IN_PROGRESS', 'READY', 'COMPLETED']")
    log(").aggregate(")
    log("    total_orders=Count('id'),")
    log("    total_revenue=Sum('total_price'),")
    log("    avg_check=Avg('total_price'),")
    log("    max_order=Max('total_price')")
    log(")")
    log()

    # Чтобы получить чистый SQL агрегации:
    from django.db import connection
    from django.test.utils import CaptureQueriesContext
    
    with CaptureQueriesContext(connection) as ctx:
        qs3 = Order.objects.filter(
            status__in=['ACCEPTED', 'IN_PROGRESS', 'READY', 'COMPLETED']
        ).aggregate(
            total_orders=Count('id'),
            total_revenue=Sum('total_price'),
            avg_check=Avg('total_price'),
            max_order=Max('total_price')
        )
        sql_agg = ctx.captured_queries[0]['sql']

    log("[Сгенерированный SQL агрегации]:")
    log(sql_agg)
    log()
    log("[Результат выполнения агрегации]:")
    log(f"1. Общее количество принятых заказов: {qs3['total_orders']} шт.")
    log(f"2. Суммарная выручка по заказам:      {qs3['total_revenue']:.2f} руб.")
    log(f"3. Средний чек клиента кондитерской:  {qs3['avg_check']:.2f} руб.")
    log(f"4. Максимальная стоимость заказа:      {qs3['max_order']:.2f} руб.")
    log()

    # -------------------------------------------------------------
    # ЗАПРОС 4: Выборка по связи «один ко многим» с select_related()
    # -------------------------------------------------------------
    log("-" * 80)
    log("ЗАПРОС 4: ВЫБОРКА ПО СВЯЗИ «ОДИН КО МНОГИМ» (select_related без проблемы N+1)")
    log("-" * 80)
    log("Бизнес-задача: Загрузить позиции заказов со статусом ACCEPTED сразу с присоединенными объектами Заказа, Клиента, Коржа и Начинки через единый SQL JOIN.")
    log()
    log("[ORM-запрос]:")
    log("qs4 = OrderItem.objects.select_related(")
    log("    'order', 'order__customer', 'crust_type', 'filling'")
    log(").filter(order__status='ACCEPTED')[:5]")
    log()
    
    qs4 = OrderItem.objects.select_related(
        'order', 'order__customer', 'crust_type', 'filling'
    ).filter(order__status='ACCEPTED')[:5]
    
    log("[Сгенерированный SQL с INNER JOIN]:")
    log(str(qs4.query))
    log()
    log("[Результат выполнения (первые 5 позиций в работе)]:")
    log(f"{'Поз.#':<6} | {'Заказ#':<7} | {'Клиент':<16} | {'Корж':<25} | {'Начинка':<30} | {'Вес':<6} | {'Цена':<10}")
    log("-" * 105)
    for it in qs4:
        c_name = it.order.customer.get_full_name() or it.order.customer.username
        cr_short = it.crust_type.name[:23] + ".." if len(it.crust_type.name) > 25 else it.crust_type.name
        fl_short = it.filling.name[:28] + ".." if len(it.filling.name) > 30 else it.filling.name
        log(f"{it.id:<6} | #{it.order.id:<6} | {c_name:<16} | {cr_short:<25} | {fl_short:<30} | {it.weight}кг | {it.item_price:>7} руб.")
    log()

    # -------------------------------------------------------------
    # ЗАПРОС 5: Выборка по связи «многие ко многим» с prefetch_related()
    # -------------------------------------------------------------
    log("-" * 80)
    log("ЗАПРОС 5: ВЫБОРКА ПО СВЯЗИ «МНОГИЕ КО МНОГИМ» (prefetch_related для M:M и 1:M)")
    log("-" * 80)
    log("Бизнес-задача: Загрузить торты категории «Классические торты» с предварительной пакетной выборкой всех совместимых начинок (M:M) и отзывов клиентов (1:M).")
    log()
    log("[ORM-запрос]:")
    log("qs5 = BaseCake.objects.prefetch_related(")
    log("    'available_fillings', 'reviews'")
    log(").filter(category__slug='classic-cakes')[:5]")
    log()
    
    with CaptureQueriesContext(connection) as ctx:
        qs5 = list(BaseCake.objects.prefetch_related(
            'available_fillings', 'reviews'
        ).filter(category__slug='classic-cakes')[:5])
        sql_prefetch = [q['sql'] for q in ctx.captured_queries]

    log(f"[Количество выполненных SQL-запросов]: {len(sql_prefetch)} (вместо N+1)")
    for i, s in enumerate(sql_prefetch, 1):
        log(f"  SQL [{i}]: {s}")
    log()
    log("[Результат выполнения выборки тортов с начинками и отзывами]:")
    for b in qs5:
        fillings_list = ", ".join([f.name for f in b.available_fillings.all()]) or "Любая начинка"
        rev_count = b.reviews.count()
        avg_r = b.reviews.aggregate(a=Avg('rating'))['a'] or 0.0
        log(f"• Торт: «{b.title}» (Цена: от {b.base_price} руб.)")
        log(f"  - Совместимые начинки M:M: {fillings_list}")
        log(f"  - Отзывы: {rev_count} шт., средний рейтинг: {avg_r:.1f} / 5.0")
        log()

    # Сохранение в файл
    output_path = BASE_DIR / 'docs' / 'day5' / 'queries_day5.txt'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(output_lines))
    log("=" * 80)
    log(f"УСПЕШНО: Все 5 запросов выполнены и сохранены в файл {output_path.relative_to(BASE_DIR)}")
    log("=" * 80)

if __name__ == "__main__":
    run_all_queries()
