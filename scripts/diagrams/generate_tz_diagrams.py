# -*- coding: utf-8 -*-
"""
Генерация графических схем для Технического задания по ГОСТ 19.201-78
1. tz_site_structure.png: Структурная схема навигации и карты веб-сервиса
2. tz_wireframe_builder.png: Схема интерфейса онлайн-конструктора десертов
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

def get_font(size, bold=False):
    font_names = [
        "arialbd.ttf" if bold else "arial.ttf",
        "tahomabd.ttf" if bold else "tahoma.ttf",
        "calibrib.ttf" if bold else "calibri.ttf"
    ]
    for fn in font_names:
        try:
            return ImageFont.truetype(fn, size)
        except:
            pass
    return ImageFont.load_default()

def draw_round_rect(draw, bbox, fill, outline, width=2, radius=8):
    x0, y0, x1, y1 = bbox
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill, outline=outline, width=width)

def draw_arrow(draw, start, end, fill="#2C3E50", width=2):
    x0, y0 = start
    x1, y1 = end
    draw.line([x0, y0, x1, y1], fill=fill, width=width)
    # Arrow head
    if x1 > x0 and y1 == y0: # Right
        draw.polygon([(x1, y1), (x1-8, y1-5), (x1-8, y1+5)], fill=fill)
    elif x1 == x0 and y1 > y0: # Down
        draw.polygon([(x1, y1), (x1-5, y1-8), (x1+5, y1-8)], fill=fill)
    elif x1 == x0 and y1 < y0: # Up
        draw.polygon([(x1, y1), (x1-5, y1+8), (x1+5, y1+8)], fill=fill)

def generate_tz_diagrams():
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    out_dir = BASE_DIR / "assets" / "diagrams"
    out_dir.mkdir(parents=True, exist_ok=True)

    f_title = get_font(18, bold=True)
    f_sub = get_font(13, bold=True)
    f_txt = get_font(11, bold=False)
    f_bold = get_font(11, bold=True)
    f_small = get_font(10, bold=False)

    # ------------------ РИСУНОК 1: КАРТА ВЕБ-СЕРВИСА ------------------
    w1, h1 = 1200, 680
    im1 = Image.new("RGB", (w1, h1), "#FFFFFF")
    d1 = ImageDraw.Draw(im1)

    # Header
    d1.rectangle([0, 0, w1, 50], fill="#1F497D")
    d1.text((w1//2, 25), "СТРУКТУРНАЯ СХЕМА НАВИГАЦИИ И КАРТЫ ВЕБ-СЕРВИСА «SWEETCRAFT»", font=f_title, fill="#FFFFFF", anchor="mm")

    # Main page node
    main_box = [w1//2 - 160, 80, w1//2 + 160, 160]
    draw_round_rect(d1, main_box, fill="#EBF2FA", outline="#1F497D", width=2, radius=10)
    d1.text((w1//2, 105), "Главная страница (/)", font=f_sub, fill="#1F497D", anchor="mm")
    d1.text((w1//2, 135), "Промо-витрина • Быстрый поиск • Переход к заказу", font=f_txt, fill="#4A5568", anchor="mm")

    # 4 Main branches
    branch_y = 230
    branches = [
        {"name": "Каталог десертов\n(/catalog/)", "sub": ["Фильтрация (3 параметра)", "Сортировка (3 критерия)", "Постраничная пагинация (20)", "Карточка торта (/cake/<slug>/)"], "x": 160, "bg": "#E8F5E9", "border": "#2E7D32"},
        {"name": "Онлайн-конструктор\n(/builder/)", "sub": ["Выбор веса (1.0-20.0 кг)", "Выбор коржа и начинки", "Декор (M:M)", "Живой калькулятор (fetch API)", "Проверка смен (35/45 кг)"], "x": 450, "bg": "#FFF8E1", "border": "#F57F17"},
        {"name": "Личный кабинет\n(/account/)", "sub": ["История заказов", "Статус изготовления", "Просмотр эскиза", "CRUD отзывов и оценок", "Повтор заказа в 1 клик"], "x": 750, "bg": "#E3F2FD", "border": "#1565C0"},
        {"name": "Служебный раздел\n(/admin/ | /shifts/)", "sub": ["Панель шеф-кондитера", "График смен ConfectionerShift", "Печать наряда (@media print)", "Экспорт реестра в CSV"], "x": 1040, "bg": "#F3E5F5", "border": "#7B1FA2"}
    ]

    # Trunk from main
    d1.line([w1//2, 160, w1//2, 195], fill="#1F497D", width=2)
    d1.line([160, 195, 1040, 195], fill="#1F497D", width=2)

    for b in branches:
        bx = b["x"]
        d1.line([bx, 195, bx, branch_y], fill="#1F497D", width=2)
        draw_arrow(d1, (bx, 195), (bx, branch_y), fill="#1F497D", width=2)

        # Branch header card
        draw_round_rect(d1, [bx-120, branch_y, bx+120, branch_y+65], fill=b["bg"], outline=b["border"], width=2, radius=8)
        lines = b["name"].split("\n")
        d1.text((bx, branch_y + 20), lines[0], font=f_sub, fill=b["border"], anchor="mm")
        d1.text((bx, branch_y + 45), lines[1], font=f_bold, fill="#2C3E50", anchor="mm")

        # Sub-items
        sub_y = branch_y + 90
        for s_idx, item in enumerate(b["sub"]):
            item_box = [bx-115, sub_y, bx+115, sub_y+42]
            draw_round_rect(d1, item_box, fill="#FFFFFF", outline="#CBD5E0", width=1, radius=6)
            d1.text((bx, sub_y+21), item, font=f_txt, fill="#2D3748", anchor="mm")
            # connector
            d1.line([bx, sub_y - 10 if s_idx == 0 else sub_y - 6, bx, sub_y], fill="#A0AEC0", width=1)
            sub_y += 50

    p1 = str(out_dir / "tz_site_structure.png")
    im1.save(p1, optimize=True)
    print(f"Saved: {p1}")

    # ------------------ РИСУНОК 2: АРХИТЕКТУРА И ИНТЕРФЕЙС КОНСТРУКТОРА ------------------
    w2, h2 = 1200, 720
    im2 = Image.new("RGB", (w2, h2), "#FFFFFF")
    d2 = ImageDraw.Draw(im2)

    # Header
    d2.rectangle([0, 0, w2, 50], fill="#1F497D")
    d2.text((w2//2, 25), "АРХИТЕКТУРНО-ФУНКЦИОНАЛЬНАЯ СХЕМА ОНЛАЙН-КОНСТРУКТОРА ТОРА И ВАЛИДАЦИИ СМЕН", font=f_title, fill="#FFFFFF", anchor="mm")

    # Left: Client UI Wireframe
    d2.rectangle([40, 80, 680, 680], outline="#4A5568", fill="#FAFAFA", width=2)
    d2.rectangle([40, 80, 680, 120], fill="#EDF2F7", outline="#CBD5E0", width=1)
    d2.text((60, 100), "БРАУЗЕР ПОЛЬЗОВАТЕЛЯ: СТРАНИЦА ОНЛАЙН-КОНСТРУКТОРА (/builder/)", font=f_sub, fill="#2B6CB0", anchor="lm")

    # Step 1: Base & Weight
    draw_round_rect(d2, [60, 140, 660, 215], fill="#FFFFFF", outline="#E2E8F0", width=1, radius=6)
    d2.text((80, 160), "1. Выбор основы и массы торта (кг):", font=f_bold, fill="#1A202C")
    d2.text((80, 185), "• Тип бисквита: [Классический шифоновый v] (+0 руб.)", font=f_txt, fill="#4A5568")
    d2.text((380, 185), "• Масса (W): [ 3.5 кг ]  (Ползунок 1.0 - 20.0 кг)", font=f_bold, fill="#2B6CB0")

    # Step 2: Filling & Decor
    draw_round_rect(d2, [60, 230, 660, 325], fill="#FFFFFF", outline="#E2E8F0", width=1, radius=6)
    d2.text((80, 250), "2. Авторская начинка и декор (M:M):", font=f_bold, fill="#1A202C")
    d2.text((80, 275), "• Начинка: [Манго-маракуйя с муссом] (Тариф: 1 800 руб./кг)", font=f_txt, fill="#4A5568")
    d2.text((80, 300), "• Дополнительный декор: [x] Ягодный венок (+650 р.)   [x] Сахарная табличка (+350 р.)", font=f_txt, fill="#276A3C")

    # Step 3: Date & Sketch
    draw_round_rect(d2, [60, 340, 660, 460], fill="#FFFFFF", outline="#E2E8F0", width=1, radius=6)
    d2.text((80, 360), "3. Дата выдачи и прикрепление эскиза:", font=f_bold, fill="#1A202C")
    d2.text((80, 385), "• Календарь даты выдачи: [ 2026-11-20 ] (Проверка смены в реальном времени)", font=f_bold, fill="#C53030")
    d2.text((80, 410), "• Загрузка фото-эскиза: [ Обзор... ] sketch_anniversary.jpg (1.8 МБ <= 5 МБ)", font=f_txt, fill="#4A5568")
    d2.text((80, 435), "• Текст поздравительной надписи: «С юбилеем, любимый папа! 50 лет»", font=f_txt, fill="#718096")

    # Live Price calculation box
    draw_round_rect(d2, [60, 480, 660, 580], fill="#EBF8FF", outline="#3182CE", width=2, radius=8)
    d2.text((80, 505), "ДИНАМИЧЕСКИЙ РАСЧЕТ ЦЕНЫ (Асинхронный fetch-запрос к API):", font=f_bold, fill="#2B6CB0")
    d2.text((80, 530), "Формула: (3.5 кг * 1 800 руб) + 0 руб + (650 руб + 350 руб) = 7 300 руб.", font=f_sub, fill="#1A365D")
    d2.text((80, 555), "Статус мощности: [ OK: На выбранную дату свободно 18.5 кг из 35.0 кг квоты цеха ]", font=f_bold, fill="#276A3C")

    # Submit button
    draw_round_rect(d2, [200, 605, 520, 660], fill="#2B6CB0", outline="#1A365D", width=2, radius=8)
    d2.text((360, 632), "ОФОРМИТЬ ЗАКАЗ В ЦЕХ", font=f_sub, fill="#FFFFFF", anchor="mm")

    # Right: Backend Server & DB Architecture
    d2.rectangle([720, 80, 1160, 680], outline="#4A5568", fill="#F7FAFC", width=2)
    d2.rectangle([720, 80, 1160, 120], fill="#2D3748", outline="#1A202C", width=1)
    d2.text((740, 100), "СЕРВЕР DJANGO (БЭКЕНД И БАЗА ДАННЫХ)", font=f_sub, fill="#FFFFFF", anchor="lm")

    # Server components
    s_boxes = [
        {"title": "1. Обработчик /api/calculate-price/", "desc": "Принимает JSON (weight, crust_id, filling_id, decor_ids)\nСчитает точную стоимость по формуле\nВозвращает ответ за < 100 мс", "y": 140, "bg": "#EDF2F7", "color": "#2B6CB0"},
        {"title": "2. Модуль контроля смен цеха", "desc": "ORM-запрос: ConfectionerShift.objects.get(date)\nСумма веса: Order.objects.filter(date).aggregate(Sum('weight'))\nБлокировка даты при остатке < weight торта", "y": 270, "bg": "#FFF5F5", "color": "#C53030"},
        {"title": "3. Атомарное сохранение (transaction.atomic)", "desc": "1. Запись Order (статус: «Принят в работу»)\n2. Создание OrderItem и привязка M:M Decoration\n3. Сохранение файла фото в media/sketches/\n4. Отправка email через send_mail()", "y": 400, "bg": "#F0FFF4", "color": "#276A3C"},
        {"title": "4. Генератор техкарты для кухни", "desc": "Формирование HTML-наряда со стилями @media print\nВывод чек-листа декора и вложенного фото-эскиза\nРаспечатка кондитером в цеху в 1 клик", "y": 550, "bg": "#FAF5FF", "color": "#6B46C1"}
    ]

    for sb in s_boxes:
        sy = sb["y"]
        draw_round_rect(d2, [740, sy, 1140, sy+105], fill=sb["bg"], outline="#CBD5E0", width=1, radius=6)
        d2.text((755, sy+20), sb["title"], font=f_bold, fill=sb["color"])
        lines = sb["desc"].split("\n")
        ly = sy + 42
        for line in lines:
            d2.text((755, ly), line, font=f_txt, fill="#4A5568")
            ly += 18

    # Arrow between client and server
    d2.line([660, 530, 740, 200], fill="#3182CE", width=3)
    draw_arrow(d2, (660, 530), (740, 200), fill="#3182CE", width=3)

    d2.line([660, 390, 740, 320], fill="#C53030", width=3)
    draw_arrow(d2, (660, 390), (740, 320), fill="#C53030", width=3)

    p2 = str(out_dir / "tz_wireframe_builder.png")
    im2.save(p2, optimize=True)
    print(f"Saved: {p2}")

if __name__ == "__main__":
    generate_tz_diagrams()
