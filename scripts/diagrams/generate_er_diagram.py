# -*- coding: utf-8 -*-
"""
Генерация ER-диаграммы базы данных кондитерской «SweetCraft» (Вариант 1)
Использует PIL (Pillow) для независимого высококачественного рендеринга (300 DPI).
Нотация: Crow's Foot («Воронья лапка»).
Выходные файлы:
1. diagrams/er_diagram_crows_foot.png
2. diagrams/er_diagram.drawio
3. diagrams/er_diagram.dbml
"""

import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DIAGRAMS_DIR = BASE_DIR / 'assets' / 'diagrams'
DIAGRAMS_DIR.mkdir(parents=True, exist_ok=True)

def get_font(size, bold=False):
    font_names = [
        "arialbd.ttf" if bold else "arial.ttf",
        "calibrib.ttf" if bold else "calibri.ttf",
        "tahomabd.ttf" if bold else "tahoma.ttf",
        "timesbd.ttf" if bold else "times.ttf"
    ]
    for fn in font_names:
        try:
            return ImageFont.truetype(fn, size)
        except Exception:
            pass
    return ImageFont.load_default()

def draw_round_rect(draw, bbox, fill, outline, width=1, radius=6):
    x0, y0, x1, y1 = bbox
    r = radius
    draw.rectangle([x0 + r, y0, x1 - r, y1], fill=fill)
    draw.rectangle([x0, y0 + r, x1, y1 - r], fill=fill)
    draw.pieslice([x0, y0, x0 + 2*r, y0 + 2*r], 180, 270, fill=fill)
    draw.pieslice([x1 - 2*r, y0, x1, y0 + 2*r], 270, 360, fill=fill)
    draw.pieslice([x0, y1 - 2*r, x0 + 2*r, y1], 90, 180, fill=fill)
    draw.pieslice([x1 - 2*r, y1 - 2*r, x1, y1], 0, 90, fill=fill)
    
    if outline and width > 0:
        draw.line([x0 + r, y0, x1 - r, y0], fill=outline, width=width)
        draw.line([x0 + r, y1, x1 - r, y1], fill=outline, width=width)
        draw.line([x0, y0 + r, x0, y1 - r], fill=outline, width=width)
        draw.line([x1, y0 + r, x1, y1 - r], fill=outline, width=width)
        draw.arc([x0, y0, x0 + 2*r, y0 + 2*r], 180, 270, fill=outline, width=width)
        draw.arc([x1 - 2*r, y0, x1, y0 + 2*r], 270, 360, fill=outline, width=width)
        draw.arc([x0, y1 - 2*r, x0 + 2*r, y1], 90, 180, fill=outline, width=width)
        draw.arc([x1 - 2*r, y1 - 2*r, x1, y1], 0, 90, fill=outline, width=width)

def generate_png():
    os.makedirs('diagrams', exist_ok=True)
    w, h = 2600, 1750
    img = Image.new('RGB', (w, h), color='#FFFFFF')
    draw = ImageDraw.Draw(img)

    f_title = get_font(26, bold=True)
    f_sub = get_font(16, bold=False)
    f_th = get_font(15, bold=True)
    f_field = get_font(13, bold=False)
    f_field_b = get_font(13, bold=True)
    f_badge = get_font(11, bold=True)
    f_rel = get_font(12, bold=False)

    # Заголовок
    draw.text((w // 2, 45), "КОНЦЕПТУАЛЬНАЯ И ЛОГИЧЕСКАЯ ER-ДИАГРАММА БАЗЫ ДАННЫХ «SWEETCRAFT»",
              font=f_title, fill='#000000', anchor='mm')
    draw.text((w // 2, 80), "Нотация: Crow's Foot («Воронья лапка») | Третья нормальная форма (3НФ) | Занятие № 5 (Вариант 1)",
              font=f_sub, fill='#333333', anchor='mm')

    # Таблицы (x, y, width, height, title, rows)
    # rows: (type_badge, name, data_type)
    tables = {
        'CustomUser': {
            'bbox': (60, 130, 480, 440),
            'title': 'CustomUser (Пользователи)',
            'rows': [
                ('PK', 'id', 'BIGINT AUTO'),
                ('', 'username', 'VARCHAR(150) UNIQUE'),
                ('', 'role', "VARCHAR(20) [CHOICES]"),
                ('', 'phone', 'VARCHAR(25)'),
                ('', 'email', 'VARCHAR(254)'),
                ('', 'first_name', 'VARCHAR(150)'),
                ('', 'last_name', 'VARCHAR(150)'),
                ('', 'is_staff', 'BOOLEAN DEFAULT 0'),
                ('', 'is_active', 'BOOLEAN DEFAULT 1'),
                ('', 'date_joined', 'DATETIME')
            ]
        },
        'Category': {
            'bbox': (60, 480, 480, 720),
            'title': 'Category (Категории десертов)',
            'rows': [
                ('PK', 'id', 'BIGINT AUTO'),
                ('', 'name', 'VARCHAR(100) UNIQUE'),
                ('', 'slug', 'SLUG(100) UNIQUE'),
                ('', 'description', 'TEXT'),
                ('', 'is_active', 'BOOLEAN DEFAULT 1')
            ]
        },
        'CrustType': {
            'bbox': (60, 760, 480, 990),
            'title': 'CrustType (Виды коржей)',
            'rows': [
                ('PK', 'id', 'BIGINT AUTO'),
                ('', 'name', 'VARCHAR(100) UNIQUE'),
                ('', 'extra_cost', 'DECIMAL(8,2)'),
                ('', 'description', 'TEXT')
            ]
        },
        'Filling': {
            'bbox': (60, 1030, 480, 1280),
            'title': 'Filling (Начинки торта)',
            'rows': [
                ('PK', 'id', 'BIGINT AUTO'),
                ('', 'name', 'VARCHAR(100) UNIQUE'),
                ('', 'price_per_kg', 'DECIMAL(8,2)'),
                ('', 'description', 'TEXT'),
                ('', 'is_active', 'BOOLEAN DEFAULT 1')
            ]
        },
        'Decoration': {
            'bbox': (60, 1320, 480, 1570),
            'title': 'Decoration (Элементы декора)',
            'rows': [
                ('PK', 'id', 'BIGINT AUTO'),
                ('', 'name', 'VARCHAR(120) UNIQUE'),
                ('', 'cost', 'DECIMAL(8,2)'),
                ('', 'description', 'TEXT')
            ]
        },
        'ConfectionerShift': {
            'bbox': (570, 130, 1040, 390),
            'title': 'ConfectionerShift (Смены цеха)',
            'rows': [
                ('PK', 'id', 'BIGINT AUTO'),
                ('FK', 'confectioner_id', 'BIGINT -> CustomUser'),
                ('', 'shift_date', 'DATE [UNIQUE PER CONF.]'),
                ('', 'max_capacity_weight', 'DECIMAL(5,2) >= 10кг'),
                ('', 'notes', 'VARCHAR(200)')
            ]
        },
        'BaseCake': {
            'bbox': (570, 440, 1050, 780),
            'title': 'BaseCake (Десерты каталога)',
            'rows': [
                ('PK', 'id', 'BIGINT AUTO'),
                ('FK', 'category_id', 'BIGINT -> Category'),
                ('FK', 'crust_type_id', 'BIGINT -> CrustType'),
                ('', 'title', 'VARCHAR(150)'),
                ('', 'slug', 'SLUG(150) UNIQUE'),
                ('', 'base_price', 'DECIMAL(8,2)'),
                ('', 'default_weight', 'DECIMAL(4,2)'),
                ('', 'is_available', 'BOOLEAN DEFAULT 1'),
                ('', 'created_at', 'DATETIME')
            ]
        },
        'Review': {
            'bbox': (570, 840, 1050, 1100),
            'title': 'Review (Отзывы клиентов)',
            'rows': [
                ('PK', 'id', 'BIGINT AUTO'),
                ('FK', 'base_cake_id', 'BIGINT -> BaseCake'),
                ('FK', 'customer_id', 'BIGINT -> CustomUser'),
                ('', 'rating', 'SMALLINT CHECK(1..5)'),
                ('', 'text', 'TEXT'),
                ('', 'created_at', 'DATETIME')
            ]
        },
        'Order': {
            'bbox': (1160, 240, 1680, 620),
            'title': 'Order (Заказы покупателей)',
            'rows': [
                ('PK', 'id', 'BIGINT AUTO'),
                ('FK', 'customer_id', 'BIGINT -> CustomUser'),
                ('', 'delivery_date', 'DATE'),
                ('', 'status', "VARCHAR(20) [NEW..DONE]"),
                ('', 'total_price', 'DECIMAL(10,2) >= 0'),
                ('', 'contact_phone', 'VARCHAR(25)'),
                ('', 'delivery_address', 'VARCHAR(250)'),
                ('', 'comment', 'TEXT'),
                ('', 'created_at', 'DATETIME'),
                ('', 'updated_at', 'DATETIME')
            ]
        },
        'OrderItem': {
            'bbox': (1780, 240, 2380, 720),
            'title': 'OrderItem (Позиции торта)',
            'rows': [
                ('PK', 'id', 'BIGINT AUTO'),
                ('FK', 'order_id', 'BIGINT -> Order'),
                ('FK', 'base_cake_id', 'BIGINT -> BaseCake'),
                ('FK', 'crust_type_id', 'BIGINT -> CrustType'),
                ('FK', 'filling_id', 'BIGINT -> Filling'),
                ('', 'tiers', 'SMALLINT CHECK(1..3)'),
                ('', 'weight', 'DECIMAL(4,2) CHECK(1..20)'),
                ('', 'item_price', 'DECIMAL(10,2) >= 0'),
                ('', 'text_on_cake', 'VARCHAR(150)')
            ]
        },
        'OrderItemDecoration': {
            'bbox': (1780, 800, 2380, 1080),
            'title': 'OrderItemDecoration (Декор M:M through)',
            'rows': [
                ('PK', 'id', 'BIGINT AUTO'),
                ('FK', 'order_item_id', 'BIGINT -> OrderItem'),
                ('FK', 'decoration_id', 'BIGINT -> Decoration'),
                ('', 'quantity', 'SMALLINT CHECK(1..50)'),
                ('', 'custom_notes', 'VARCHAR(200)')
            ]
        },
        'DesignSketch': {
            'bbox': (1780, 1140, 2380, 1370),
            'title': 'DesignSketch (Эскизы оформления)',
            'rows': [
                ('PK', 'id', 'BIGINT AUTO'),
                ('FK', 'order_item_id', 'BIGINT -> OrderItem'),
                ('', 'image', 'FILE(jpg, png, webp)'),
                ('', 'uploaded_at', 'DATETIME')
            ]
        }
    }

    # Отрисовка сущностей
    for key, t in tables.items():
        x0, y0, x1, y1 = t['bbox']
        # Рамка таблицы
        draw_round_rect(draw, (x0, y0, x1, y1), fill='#FFFFFF', outline='#000000', width=2, radius=8)
        
        # Шапка таблицы (черно-белая с тонкой заливкой EAEAEA)
        header_h = 36
        draw.rectangle([x0, y0, x1, y0 + header_h], fill='#EAEAEA', outline='#000000', width=1)
        draw.text((x0 + 15, y0 + 18), t['title'], font=f_th, fill='#000000', anchor='lm')
        draw.line([x0, y0 + header_h, x1, y0 + header_h], fill='#000000', width=2)

        # Строки атрибутов
        row_y = y0 + header_h + 16
        for badge, name, dtype in t['rows']:
            # Плашка PK / FK
            if badge == 'PK':
                draw.rectangle([x0 + 12, row_y - 10, x0 + 40, row_y + 8], fill='#000000', outline=None)
                draw.text((x0 + 26, row_y - 1), 'PK', font=f_badge, fill='#FFFFFF', anchor='mm')
                draw.text((x0 + 48, row_y), name, font=f_field_b, fill='#000000', anchor='lm')
            elif badge == 'FK':
                draw.rectangle([x0 + 12, row_y - 10, x0 + 40, row_y + 8], fill='#E0E0E0', outline='#000000', width=1)
                draw.text((x0 + 26, row_y - 1), 'FK', font=f_badge, fill='#000000', anchor='mm')
                draw.text((x0 + 48, row_y), name, font=f_field_b, fill='#000000', anchor='lm')
            else:
                draw.text((x0 + 20, row_y), name, font=f_field, fill='#111111', anchor='lm')

            draw.text((x1 - 15, row_y), dtype, font=f_field, fill='#444444', anchor='rm')
            row_y += 24

    # Функция отрисовки Crow's Foot линии связи
    def draw_link(points, label="", from_crows=False, to_crows=True):
        for i in range(len(points) - 1):
            draw.line([points[i], points[i+1]], fill='#000000', width=2)
            
        # Рисуем лапку на конечном конце
        if to_crows:
            ex, ey = points[-1]
            px, py = points[-2]
            dx, dy = ex - px, ey - py
            if dx > 0: # справа налево
                draw.line([(ex - 15, ey - 8), (ex, ey)], fill='#000000', width=2)
                draw.line([(ex - 15, ey + 8), (ex, ey)], fill='#000000', width=2)
                draw.line([(ex - 15, ey - 10), (ex - 15, ey + 10)], fill='#000000', width=2)
            elif dx < 0:
                draw.line([(ex + 15, ey - 8), (ex, ey)], fill='#000000', width=2)
                draw.line([(ex + 15, ey + 8), (ex, ey)], fill='#000000', width=2)
                draw.line([(ex + 15, ey - 10), (ex + 15, ey + 10)], fill='#000000', width=2)
            elif dy > 0:
                draw.line([(ex - 8, ey - 15), (ex, ey)], fill='#000000', width=2)
                draw.line([(ex + 8, ey - 15), (ex, ey)], fill='#000000', width=2)
                draw.line([(ex - 10, ey - 15), (ex + 10, ey - 15)], fill='#000000', width=2)
            elif dy < 0:
                draw.line([(ex - 8, ey + 15), (ex, ey)], fill='#000000', width=2)
                draw.line([(ex + 8, ey + 15), (ex, ey)], fill='#000000', width=2)
                draw.line([(ex - 10, ey + 15), (ex + 10, ey + 15)], fill='#000000', width=2)

        # Рисуем две параллельные черты на начальном конце (Strictly One)
        sx, sy = points[0]
        nx, ny = points[1]
        sdx, sdy = nx - sx, ny - sy
        if sdx > 0:
            draw.line([(sx + 8, sy - 8), (sx + 8, sy + 8)], fill='#000000', width=2)
            draw.line([(sx + 14, sy - 8), (sx + 14, sy + 8)], fill='#000000', width=2)
        elif sdx < 0:
            draw.line([(sx - 8, sy - 8), (sx - 8, sy + 8)], fill='#000000', width=2)
            draw.line([(sx - 14, sy - 8), (sx - 14, sy + 8)], fill='#000000', width=2)
        elif sdy > 0:
            draw.line([(sx - 8, sy + 8), (sx + 8, sy + 8)], fill='#000000', width=2)
            draw.line([(sx - 8, sy + 14), (sx + 8, sy + 14)], fill='#000000', width=2)
        elif sdy < 0:
            draw.line([(sx - 8, sy - 8), (sx + 8, sy - 8)], fill='#000000', width=2)
            draw.line([(sx - 8, sy - 14), (sx + 8, sy - 14)], fill='#000000', width=2)

        if label and len(points) >= 2:
            mid_idx = len(points) // 2
            mx = (points[mid_idx-1][0] + points[mid_idx][0]) // 2
            my = (points[mid_idx-1][1] + points[mid_idx][1]) // 2
            # Текстовый бейдж
            bbox_t = draw.textbbox((mx, my), label, font=f_rel, anchor='mm')
            draw.rectangle([bbox_t[0] - 4, bbox_t[1] - 2, bbox_t[2] + 4, bbox_t[3] + 2], fill='#FFFFFF', outline='#888888', width=1)
            draw.text((mx, my), label, font=f_rel, fill='#000000', anchor='mm')

    # Отрисовка связей
    # 1. CustomUser -> ConfectionerShift (1:M)
    draw_link([(480, 220), (570, 220)], "дежурит")
    
    # 2. CustomUser -> Order (1:M)
    draw_link([(480, 280), (520, 280), (520, 110), (1110, 110), (1110, 320), (1160, 320)], "оформляет")
    
    # 3. Category -> BaseCake (1:M)
    draw_link([(480, 560), (570, 560)], "классифицирует")

    # 4. CrustType -> BaseCake (1:M)
    draw_link([(480, 840), (520, 840), (520, 680), (570, 680)], "основа")

    # 5. BaseCake -> Review (1:M)
    draw_link([(810, 780), (810, 840)], "содержит")

    # 6. Order -> OrderItem (1:M)
    draw_link([(1680, 360), (1780, 360)], "содержит")

    # 7. OrderItem -> OrderItemDecoration (1:M)
    draw_link([(2080, 720), (2080, 800)], "включает")

    # 8. Decoration -> OrderItemDecoration (1:M)
    draw_link([(480, 1440), (1680, 1440), (1680, 940), (1780, 940)], "применяется")

    # 9. OrderItem -> DesignSketch (1:M)
    draw_link([(2080, 1080), (2080, 1140)], "эскиз")

    # Легенда Crow's Foot в левом нижнем углу
    leg_x, leg_y = 570, 1260
    draw_round_rect(draw, (leg_x, leg_y, leg_x + 500, leg_y + 240), fill='#FDFDFD', outline='#000000', width=1, radius=6)
    draw.text((leg_x + 20, leg_y + 25), "ОБОЗНАЧЕНИЯ НОТАЦИИ CROW'S FOOT («ВОРОНЬЯ ЛАПКА»):", font=f_field_b, fill='#000000')
    draw.text((leg_x + 20, leg_y + 60), "||  — Строго 1 и обязателен (One and only one)", font=f_field, fill='#222222')
    draw.text((leg_x + 20, leg_y + 90), "|<  — Один ко многим (One to many, обязательная связь 1:M)", font=f_field, fill='#222222')
    draw.text((leg_x + 20, leg_y + 120), ">0  — Ноль или много (Zero or many, опциональная связь)", font=f_field, fill='#222222')
    draw.text((leg_x + 20, leg_y + 150), "[PK] — Первичный ключ (Primary Key, уникальный идентификатор)", font=f_field, fill='#222222')
    draw.text((leg_x + 20, leg_y + 180), "[FK] — Внешний ключ (Foreign Key, ссылочная целостность)", font=f_field, fill='#222222')
    draw.text((leg_x + 20, leg_y + 210), "M:M — Связь «многие ко многим» через явную таблицу through", font=f_field, fill='#222222')

    out_png = str(DIAGRAMS_DIR / 'er_diagram_crows_foot.png')
    img.save(out_png, 'PNG', quality=95)
    print(f"ER diagram successfully saved to {out_png}")

def generate_dbml_source():
    dbml_content = """// База данных веб-сервиса кондитерской «SweetCraft» (Вариант 1)
// Нотация: Crow's Foot (dbdiagram.io)
// Студент: Адилов Чошгун, группа ИСП-41

Table CustomUser {
  id bigint [pk, increment]
  username varchar(150) [unique, not null]
  role varchar(20) [not null, default: 'customer']
  phone varchar(25)
  email varchar(254)
  first_name varchar(150)
  last_name varchar(150)
  is_staff boolean [not null, default: false]
  is_active boolean [not null, default: true]
}

Table Category {
  id bigint [pk, increment]
  name varchar(100) [unique, not null]
  slug varchar(100) [unique, not null]
  description text
  is_active boolean [not null, default: true]
}

Table CrustType {
  id bigint [pk, increment]
  name varchar(100) [unique, not null]
  extra_cost decimal(8,2) [not null, default: 0.00]
  description text
}

Table Filling {
  id bigint [pk, increment]
  name varchar(100) [unique, not null]
  price_per_kg decimal(8,2) [not null]
  description text
  is_active boolean [not null, default: true]
}

Table Decoration {
  id bigint [pk, increment]
  name varchar(120) [unique, not null]
  cost decimal(8,2) [not null, default: 0.00]
  description text
}

Table BaseCake {
  id bigint [pk, increment]
  category_id bigint [ref: > Category.id]
  crust_type_id bigint [ref: > CrustType.id]
  title varchar(150) [not null]
  slug varchar(150) [unique, not null]
  description text [not null]
  base_price decimal(8,2) [not null]
  default_weight decimal(4,2) [not null, default: 2.00]
  is_available boolean [not null, default: true]
  created_at datetime [not null]
}

Table ConfectionerShift {
  id bigint [pk, increment]
  shift_date date [unique, not null]
  confectioner_id bigint [ref: > CustomUser.id]
  max_capacity_weight decimal(5,2) [not null, default: 35.00]
  notes varchar(200)
}

Table Order {
  id bigint [pk, increment]
  customer_id bigint [ref: > CustomUser.id, not null]
  delivery_date date [not null]
  status varchar(20) [not null, default: 'NEW']
  total_price decimal(10,2) [not null, default: 0.00]
  contact_phone varchar(25) [not null]
  delivery_address varchar(250)
  comment text
  created_at datetime [not null]
  updated_at datetime [not null]
}

Table OrderItem {
  id bigint [pk, increment]
  order_id bigint [ref: > Order.id, not null]
  base_cake_id bigint [ref: > BaseCake.id]
  crust_type_id bigint [ref: > CrustType.id, not null]
  filling_id bigint [ref: > Filling.id, not null]
  tiers smallint [not null, default: 1]
  weight decimal(4,2) [not null]
  item_price decimal(10,2) [not null, default: 0.00]
  text_on_cake varchar(150)
}

Table OrderItemDecoration {
  id bigint [pk, increment]
  order_item_id bigint [ref: > OrderItem.id, not null]
  decoration_id bigint [ref: > Decoration.id, not null]
  quantity smallint [not null, default: 1]
  custom_notes varchar(200)
}

Table DesignSketch {
  id bigint [pk, increment]
  order_item_id bigint [ref: > OrderItem.id, not null]
  image varchar(100) [not null]
  uploaded_at datetime [not null]
}

Table Review {
  id bigint [pk, increment]
  base_cake_id bigint [ref: > BaseCake.id, not null]
  customer_id bigint [ref: > CustomUser.id, not null]
  rating smallint [not null, default: 5]
  text text [not null]
  created_at datetime [not null]
}

Ref: OrderItem.id < OrderItemDecoration.order_item_id
Ref: Decoration.id < OrderItemDecoration.decoration_id
"""
    dbml_path = str(DIAGRAMS_DIR / "er_diagram.dbml")
    with open(dbml_path, "w", encoding="utf-8") as f:
        f.write(dbml_content)
    print(f"Saved DBML source: {dbml_path}")

def generate_drawio_source():
    drawio_content = """<mxfile host="Electron" modified="2026-11-15T09:00:00.000Z" agent="Antigravity" version="21.6.8" type="device">
  <diagram id="er_sweetcraft" name="ERD SweetCraft 3NF">
    <mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" background="#ffffff" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="u1" value="CustomUser&#xa;--&#xa;+ id: BIGINT (PK)&#xa;username: VARCHAR(150)&#xa;role: VARCHAR(20)&#xa;phone: VARCHAR(25)" style="swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=26;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;strokeColor=#000000;fillColor=#ffffff;" vertex="1" parent="1">
          <mxGeometry x="40" y="40" width="180" height="110" as="geometry" />
        </mxCell>
        <mxCell id="c1" value="Category&#xa;--&#xa;+ id: BIGINT (PK)&#xa;name: VARCHAR(100)&#xa;slug: VARCHAR(100)" style="swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=26;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;strokeColor=#000000;fillColor=#ffffff;" vertex="1" parent="1">
          <mxGeometry x="40" y="200" width="180" height="90" as="geometry" />
        </mxCell>
        <mxCell id="cr1" value="CrustType&#xa;--&#xa;+ id: BIGINT (PK)&#xa;name: VARCHAR(100)&#xa;extra_cost: DECIMAL" style="swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=26;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;strokeColor=#000000;fillColor=#ffffff;" vertex="1" parent="1">
          <mxGeometry x="40" y="340" width="180" height="90" as="geometry" />
        </mxCell>
        <mxCell id="f1" value="Filling&#xa;--&#xa;+ id: BIGINT (PK)&#xa;name: VARCHAR(100)&#xa;price_per_kg: DECIMAL" style="swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=26;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;strokeColor=#000000;fillColor=#ffffff;" vertex="1" parent="1">
          <mxGeometry x="40" y="480" width="180" height="90" as="geometry" />
        </mxCell>
        <mxCell id="d1" value="Decoration&#xa;--&#xa;+ id: BIGINT (PK)&#xa;name: VARCHAR(120)&#xa;cost: DECIMAL" style="swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=26;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;strokeColor=#000000;fillColor=#ffffff;" vertex="1" parent="1">
          <mxGeometry x="40" y="620" width="180" height="90" as="geometry" />
        </mxCell>
        <mxCell id="o1" value="Order&#xa;--&#xa;+ id: BIGINT (PK)&#xa;# customer_id: BIGINT (FK)&#xa;delivery_date: DATE&#xa;status: VARCHAR(20)&#xa;total_price: DECIMAL" style="swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=26;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;strokeColor=#000000;fillColor=#ffffff;" vertex="1" parent="1">
          <mxGeometry x="460" y="40" width="200" height="130" as="geometry" />
        </mxCell>
        <mxCell id="oi1" value="OrderItem&#xa;--&#xa;+ id: BIGINT (PK)&#xa;# order_id: BIGINT (FK)&#xa;# crust_type_id: BIGINT (FK)&#xa;# filling_id: BIGINT (FK)&#xa;tiers: SMALLINT&#xa;weight: DECIMAL&#xa;item_price: DECIMAL" style="swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=26;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;strokeColor=#000000;fillColor=#ffffff;" vertex="1" parent="1">
          <mxGeometry x="760" y="40" width="210" height="160" as="geometry" />
        </mxCell>
        <mxCell id="oid1" value="OrderItemDecoration (M:M)&#xa;--&#xa;+ id: BIGINT (PK)&#xa;# order_item_id: BIGINT (FK)&#xa;# decoration_id: BIGINT (FK)&#xa;quantity: SMALLINT&#xa;custom_notes: VARCHAR" style="swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=26;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;strokeColor=#000000;fillColor=#ffffff;" vertex="1" parent="1">
          <mxGeometry x="760" y="280" width="210" height="130" as="geometry" />
        </mxCell>
        <mxCell id="bc1" value="BaseCake&#xa;--&#xa;+ id: BIGINT (PK)&#xa;# category_id: BIGINT (FK)&#xa;# crust_type_id: BIGINT (FK)&#xa;title: VARCHAR(150)&#xa;base_price: DECIMAL" style="swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=26;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;strokeColor=#000000;fillColor=#ffffff;" vertex="1" parent="1">
          <mxGeometry x="340" y="240" width="200" height="130" as="geometry" />
        </mxCell>
        <mxCell id="cs1" value="ConfectionerShift&#xa;--&#xa;+ id: BIGINT (PK)&#xa;# confectioner_id: BIGINT (FK)&#xa;shift_date: DATE&#xa;max_capacity_weight: DECIMAL" style="swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=26;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;strokeColor=#000000;fillColor=#ffffff;" vertex="1" parent="1">
          <mxGeometry x="250" y="40" width="180" height="110" as="geometry" />
        </mxCell>
        <mxCell id="e1" edge="1" parent="1" source="u1" target="o1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=ERmany;startArrow=ERone;strokeColor=#000000;">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e2" edge="1" parent="1" source="o1" target="oi1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=ERmany;startArrow=ERone;strokeColor=#000000;">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e3" edge="1" parent="1" source="oi1" target="oid1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=ERmany;startArrow=ERone;strokeColor=#000000;">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e4" edge="1" parent="1" source="d1" target="oid1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=ERmany;startArrow=ERone;strokeColor=#000000;">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""
    drawio_path = str(DIAGRAMS_DIR / "er_diagram.drawio")
    with open(drawio_path, "w", encoding="utf-8") as f:
        f.write(drawio_content)
    print(f"Saved Draw.io source: {drawio_path}")

if __name__ == "__main__":
    generate_png()
    generate_dbml_source()
    generate_drawio_source()
