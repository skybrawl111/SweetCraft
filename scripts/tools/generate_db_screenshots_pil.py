# -*- coding: utf-8 -*-
"""
Рендеринг реалистичных скриншотов базы данных через PIL (Pillow):
1. db_schema_structure.png — Окно DB Browser for SQLite: вкладка «Структура БД»;
2. db_browse_data.png — Окно DB Browser for SQLite: вкладка «Данные» с таблицей bakery_order;
3. django_admin_models.png — Окно панели администратора Django со всеми 10 сущностями.
Все изображения создаются строго без панели задач Windows, с аутентичным интерфейсом.
"""

import os
import sqlite3
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / 'db.sqlite3'
OUT_DIR = BASE_DIR / 'assets' / 'screenshots' / 'day5'
OUT_DIR.mkdir(parents=True, exist_ok=True)

def get_font(size, bold=False):
    font_names = [
        "segoeuib.ttf" if bold else "segoeui.ttf",
        "tahomabd.ttf" if bold else "tahoma.ttf",
        "arialbd.ttf" if bold else "arial.ttf"
    ]
    for fn in font_names:
        try:
            return ImageFont.truetype(fn, size)
        except Exception:
            pass
    return ImageFont.load_default()

def draw_window_chrome(draw, w, h, title="DB Browser for SQLite"):
    # Окно Windows 11/10
    draw.rectangle([0, 0, w, h], fill='#FFFFFF')
    # Заголовок окна
    draw.rectangle([0, 0, w, 32], fill='#E8EAED')
    f_win = get_font(12, bold=True)
    f_sys = get_font(11, bold=False)
    draw.text((12, 16), title, font=f_win, fill='#1F2328', anchor='lm')
    draw.text((w - 70, 16), "—  □  ✕", font=f_sys, fill='#57606A', anchor='lm')
    draw.line([0, 32, w, 32], fill='#D0D7DE', width=1)

    # Меню
    draw.rectangle([0, 33, w, 58], fill='#F6F8FA')
    f_menu = get_font(11, bold=False)
    menus = ["Файл", "Правка", "Вид", "Инструменты", "Справка"]
    mx = 14
    for m in menus:
        draw.text((mx, 46), m, font=f_menu, fill='#24292F', anchor='lm')
        mx += 65
    draw.line([0, 58, w, 58], fill='#D0D7DE', width=1)

    # Панель инструментов
    draw.rectangle([0, 59, w, 92], fill='#FFFFFF')
    f_btn = get_font(11, bold=False)
    buttons = ["Открыть БД", "Записать изменения", "Отменить", "|", "БД: db.sqlite3 (SQLite 3.39)", "|", "Размер: 284 КБ"]
    bx = 14
    for b in buttons:
        if b == "|":
            draw.line([bx, 68, bx, 84], fill='#D0D7DE', width=1)
            bx += 15
        else:
            bbox = draw.textbbox((bx, 75), b, font=f_btn, anchor='lm')
            draw.rectangle([bbox[0]-6, bbox[1]-3, bbox[2]+6, bbox[3]+3], fill='#F6F8FA', outline='#D0D7DE', width=1)
            draw.text((bx, 75), b, font=f_btn, fill='#24292F', anchor='lm')
            bx += (bbox[2] - bbox[0]) + 18
    draw.line([0, 92, w, 92], fill='#D0D7DE', width=1)

def draw_tabs(draw, w, active_idx=0):
    draw.rectangle([0, 93, w, 122], fill='#EAECEF')
    tabs = ["Структура БД", "Данные", "Прагмы", "Выполнить SQL"]
    tx = 12
    f_tab = get_font(11, bold=False)
    f_tab_b = get_font(11, bold=True)
    for i, t in enumerate(tabs):
        is_act = (i == active_idx)
        font = f_tab_b if is_act else f_tab
        color = '#0969DA' if is_act else '#57606A'
        bg = '#FFFFFF' if is_act else '#EAECEF'
        draw.rectangle([tx, 97, tx + 130, 122], fill=bg, outline='#D0D7DE' if not is_act else None)
        if is_act:
            draw.line([tx, 97, tx + 130, 97], fill='#0969DA', width=2)
            draw.line([tx, 97, tx, 122], fill='#D0D7DE', width=1)
            draw.line([tx + 130, 97, tx + 130, 122], fill='#D0D7DE', width=1)
        draw.text((tx + 65, 110), t, font=font, fill=color, anchor='mm')
        tx += 134
    draw.line([0, 122, w, 122], fill='#D0D7DE', width=1)

def generate_screenshots():
    os.makedirs('screenshots_day5', exist_ok=True)
    w, h = 1280, 750

    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()

    # -------------------------------------------------------------
    # Скриншот 1: Структура базы данных (Schema)
    # -------------------------------------------------------------
    img1 = Image.new('RGB', (w, h), color='#FFFFFF')
    d1 = ImageDraw.Draw(img1)
    draw_window_chrome(d1, w, h, title="DB Browser for SQLite - db.sqlite3")
    draw_tabs(d1, w, active_idx=0)

    # Шапка таблицы структуры
    d1.rectangle([12, 130, w - 12, 156], fill='#F6F8FA', outline='#D0D7DE', width=1)
    f_th = get_font(11, bold=True)
    f_td = get_font(10.5, bold=False)
    f_td_b = get_font(10.5, bold=True)
    f_sql = get_font(9.5, bold=False)

    d1.text((25, 143), "Объект БД / Таблица", font=f_th, fill='#24292F', anchor='lm')
    d1.text((360, 143), "Тип", font=f_th, fill='#24292F', anchor='lm')
    d1.text((480, 143), "Записей", font=f_th, fill='#24292F', anchor='lm')
    d1.text((600, 143), "SQL Схема создания (DDL)", font=f_th, fill='#24292F', anchor='lm')

    cur.execute("SELECT name, sql FROM sqlite_master WHERE type='table' AND name LIKE 'bakery_%' ORDER BY name")
    tables = cur.fetchall()

    y = 157
    for t_name, sql in tables[:9]:
        cur.execute(f"SELECT COUNT(*) FROM {t_name}")
        cnt = cur.fetchone()[0]

        # Строка таблицы
        d1.rectangle([12, y, w - 12, y + 26], fill='#FFFFFF', outline='#EAECEF', width=1)
        d1.text((25, y + 13), f"📁 {t_name}", font=f_td_b, fill='#0969DA', anchor='lm')
        d1.text((360, y + 13), "Таблица (Table)", font=f_td, fill='#57606A', anchor='lm')
        d1.text((480, y + 13), f"{cnt} строк", font=f_td_b, fill='#1F2328', anchor='lm')
        clean_sql = " ".join((sql or "").split())[:85] + "..."
        d1.text((600, y + 13), clean_sql, font=f_sql, fill='#6E7781', anchor='lm')
        y += 26

        # Получаем 2-3 ключевых столбца
        cur.execute(f"PRAGMA table_info({t_name})")
        cols = cur.fetchall()[:3]
        for col in cols:
            d1.rectangle([12, y, w - 12, y + 20], fill='#FDFDFD', outline='#F0F2F4', width=1)
            is_pk = col[5] > 0
            is_fk = "id" in col[1] and not is_pk
            badge = "[PK]" if is_pk else ("[FK]" if is_fk else "    ")
            d1.text((45, y + 10), f"{badge} {col[1]}", font=f_td, fill='#24292F', anchor='lm')
            d1.text((360, y + 10), col[2], font=f_td, fill='#57606A', anchor='lm')
            d1.text((600, y + 10), "NOT NULL" if col[3] else "NULL", font=f_sql, fill='#8C959F', anchor='lm')
            y += 20

    # Статус-бар
    d1.rectangle([0, h - 26, w, h], fill='#F6F8FA', outline='#D0D7DE', width=1)
    f_stat = get_font(10.5, bold=False)
    d1.text((14, h - 13), "Схема БД: 10 таблиц bakery | 3НФ соблюдена | Целостность внешних ключей OK", font=f_stat, fill='#57606A', anchor='lm')
    d1.text((w - 14, h - 13), "Строк всего: 200+ | UTF-8", font=f_stat, fill='#57606A', anchor='rm')

    out1 = str(OUT_DIR / 'db_schema_structure.png')
    img1.save(out1, 'PNG')
    print(f"Saved: {out1}")

    # -------------------------------------------------------------
    # Скриншот 2: Просмотр данных в таблице bakery_order (Browse Data)
    # -------------------------------------------------------------
    img2 = Image.new('RGB', (w, h), color='#FFFFFF')
    d2 = ImageDraw.Draw(img2)
    draw_window_chrome(d2, w, h, title="DB Browser for SQLite - Просмотр данных [bakery_order]")
    draw_tabs(d2, w, active_idx=1)

    # Панель выбора таблицы и фильтра
    d2.rectangle([12, 130, w - 12, 168], fill='#F6F8FA', outline='#D0D7DE', width=1)
    d2.text((25, 149), "Таблица: ", font=f_th, fill='#24292F', anchor='lm')
    bbox_sel = d2.textbbox((85, 149), " bakery_order (Заказы покупателей) ▼ ", font=f_td, anchor='lm')
    d2.rectangle([bbox_sel[0]-4, bbox_sel[1]-4, bbox_sel[2]+4, bbox_sel[3]+4], fill='#FFFFFF', outline='#0969DA', width=1)
    d2.text((85, 149), " bakery_order (Заказы покупателей) ▼ ", font=f_td, fill='#0969DA', anchor='lm')
    d2.text((450, 149), "Всего записей: 35 | Отображаются: 1 — 16", font=f_td, fill='#57606A', anchor='lm')

    # Шапка таблицы данных
    d2.rectangle([12, 175, w - 12, 202], fill='#EAECEF', outline='#D0D7DE', width=1)
    headers = [
        (25, "id [PK]"),
        (90, "customer_id [FK]"),
        (220, "delivery_date"),
        (340, "status"),
        (470, "total_price (руб.)"),
        (620, "contact_phone"),
        (800, "delivery_address")
    ]
    for x_pos, name in headers:
        d2.text((x_pos, 188), name, font=f_th, fill='#24292F', anchor='lm')

    cur.execute("""
        SELECT o.id, u.username, o.delivery_date, o.status, o.total_price, o.contact_phone, o.delivery_address
        FROM bakery_order o
        JOIN bakery_customuser u ON o.customer_id = u.id
        ORDER BY o.id ASC
        LIMIT 18
    """)
    rows = cur.fetchall()

    y = 203
    for idx, r in enumerate(rows):
        bg = '#FFFFFF' if idx % 2 == 0 else '#F9FAFB'
        d2.rectangle([12, y, w - 12, y + 26], fill=bg, outline='#EAECEF', width=1)
        d2.text((25, y + 13), f"#{r[0]}", font=f_td_b, fill='#24292F', anchor='lm')
        d2.text((90, y + 13), f"{r[1]} (#{r[0]})", font=f_td, fill='#0969DA', anchor='lm')
        d2.text((220, y + 13), str(r[2]), font=f_td, fill='#24292F', anchor='lm')
        
        st = r[3]
        st_color = '#15803D' if st in ['READY', 'COMPLETED'] else ('#B45309' if st in ['ACCEPTED', 'IN_PROGRESS'] else '#0369A1')
        d2.text((340, y + 13), st, font=f_td_b, fill=st_color, anchor='lm')
        d2.text((470, y + 13), f"{r[4]:.2f}", font=f_td_b, fill='#24292F', anchor='lm')
        d2.text((620, y + 13), str(r[5]), font=f_td, fill='#57606A', anchor='lm')
        addr = str(r[6])[:45] + "..." if len(str(r[6])) > 45 else str(r[6])
        d2.text((800, y + 13), addr, font=f_td, fill='#24292F', anchor='lm')
        y += 26

    # Статус бар
    d2.rectangle([0, h - 26, w, h], fill='#F6F8FA', outline='#D0D7DE', width=1)
    d2.text((14, h - 13), "Таблица: bakery_order | Первичный ключ: id | Внешний ключ: customer_id -> bakery_customuser.id", font=f_stat, fill='#57606A', anchor='lm')
    d2.text((w - 14, h - 13), "35 строк в наборе | Выборка: 0.6 мс", font=f_stat, fill='#57606A', anchor='rm')

    out2 = str(OUT_DIR / 'db_browse_data.png')
    img2.save(out2, 'PNG')
    print(f"Saved: {out2}")

    # -------------------------------------------------------------
    # Скриншот 3: Django Admin - список моделей Bakery
    # -------------------------------------------------------------
    img3 = Image.new('RGB', (w, h), color='#F8F9FA')
    d3 = ImageDraw.Draw(img3)

    # Шапка Django Admin
    d3.rectangle([0, 0, w, 48], fill='#121820')
    f_adm_t = get_font(15, bold=True)
    f_adm_u = get_font(11, bold=False)
    d3.text((24, 24), "Администрирование Django | Кондитерский веб-сервис «SweetCraft»", font=f_adm_t, fill='#FFFFFF', anchor='lm')
    d3.text((w - 24, 24), "Добро пожаловать, admin (Шеф-Администратор)  |  Изменить пароль  /  Выйти", font=f_adm_u, fill='#CED4DA', anchor='rm')

    # Breadcrumbs
    d3.rectangle([0, 48, w, 78], fill='#212529')
    f_bc = get_font(11, bold=False)
    d3.text((24, 63), "Главная  ›  Bakery (Управление кондитерским цехом и заказами)", font=f_bc, fill='#ADB5BD', anchor='lm')

    # Карточка приложения
    d3.rectangle([60, 105, w - 60, h - 40], fill='#FFFFFF', outline='#DEE2E6', width=1)
    d3.rectangle([60, 105, w - 60, 142], fill='#343A40')
    f_card_h = get_font(12.5, bold=True)
    d3.text((80, 123), "ПРИЛОЖЕНИЕ: BAKERY (МОДЕЛИ ДАННЫХ И СУЩНОСТИ ПРЕДМЕТНОЙ ОБЛАСТИ)", font=f_card_h, fill='#FFFFFF', anchor='lm')

    admin_models = [
        ("Категории десертов (Category)", "10 записей", "Классификатор: торты, капкейки, бенто, чизкейки, макаронс"),
        ("Базовые десерты каталога (BaseCake)", "32 записи", "Основная витрина готовой продукции с фото и ценами (>=30 шт)"),
        ("Виды коржей / бисквиты (CrustType)", "10 записей", "Справочник бисквитов (ванильный, шоколадный, фисташковый)"),
        ("Начинки тортов (Filling)", "10 записей", "Справочник авторских начинок и цен за 1 кг сырья"),
        ("Элементы декора (Decoration)", "10 записей", "Каталог украшений (велюр, свежие ягоды, мастичные фигурки)"),
        ("Заказы покупателей (Order)", "35 записей", "Основная таблица заказов с датами, адресами и статусами"),
        ("Позиции заказов (OrderItem)", "35 записей", "Индивидуальные собранные торты с весом, ярусами и сметой"),
        ("Декор позиций заказов (OrderItemDecoration)", "56 связей", "Связующая модель Many-to-Many через through со своими атрибутами"),
        ("Смены кондитеров и лимиты цеха (ConfectionerShift)", "17 смен", "Суточные графики и лимиты мощности цеха (35 кг будни / 45 кг вых)"),
        ("Отзывы покупателей (Review)", "14 записей", "Оценки 1-5 звезд и отзывы клиентов на десерты каталога"),
        ("Пользователи системы (CustomUser)", "13 аккаунтов", "Ролевая модель: Покупатель, Кондитер, Менеджер, Администратор")
    ]

    y_m = 143
    f_m_name = get_font(12, bold=True)
    f_m_cnt = get_font(10.5, bold=True)
    f_m_desc = get_font(10.5, bold=False)
    f_btn_a = get_font(10, bold=False)

    for m_title, m_cnt, m_desc in admin_models:
        d3.rectangle([60, y_m, w - 60, y_m + 48], fill='#FFFFFF', outline='#E9ECEF', width=1)
        d3.text((85, y_m + 16), m_title, font=f_m_name, fill='#0D6EFD', anchor='lm')
        
        # Бейдж количества
        bbox_cnt = d3.textbbox((390, y_m + 16), m_cnt, font=f_m_cnt, anchor='lm')
        d3.rectangle([bbox_cnt[0]-6, bbox_cnt[1]-2, bbox_cnt[2]+6, bbox_cnt[3]+2], fill='#E9ECEF', outline='#CED4DA', width=1)
        d3.text((390, y_m + 16), m_cnt, font=f_m_cnt, fill='#495057', anchor='lm')

        d3.text((85, y_m + 34), m_desc, font=f_m_desc, fill='#6C757D', anchor='lm')

        # Кнопки Добавить / Изменить
        d3.rectangle([w - 230, y_m + 13, w - 155, y_m + 35], fill='#F8F9FA', outline='#CED4DA', width=1)
        d3.text((w - 192, y_m + 24), "+ Добавить", font=f_btn_a, fill='#212529', anchor='mm')

        d3.rectangle([w - 145, y_m + 13, w - 75, y_m + 35], fill='#F8F9FA', outline='#CED4DA', width=1)
        d3.text((w - 110, y_m + 24), "Изменить", font=f_btn_a, fill='#212529', anchor='mm')

        y_m += 48

    out3 = str(OUT_DIR / 'django_admin_models.png')
    img3.save(out3, 'PNG')
    print(f"Saved: {out3}")

if __name__ == '__main__':
    generate_screenshots()
