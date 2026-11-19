# -*- coding: utf-8 -*-
"""
Генерация графических схем и исходников Draw.io для Занятия 6:
1. Структурная схема страниц сайта с уровнями доступа (site_structure_day6.png, .drawio)
2. Три сценария использования User Flow с ветвлениями и ошибками (user_flows_day6.png, .drawio)
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent.parent.parent
OUT_DIR = BASE_DIR / "assets" / "diagrams"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def get_font(size, bold=False):
    font_names = [
        "segoeuib.ttf" if bold else "segoeui.ttf",
        "arialbd.ttf" if bold else "arial.ttf",
        "tahomabd.ttf" if bold else "tahoma.ttf"
    ]
    for fn in font_names:
        try:
            return ImageFont.truetype(fn, size)
        except Exception:
            pass
    return ImageFont.load_default()

def draw_round_rect(draw, bbox, fill, outline, width=1, radius=6):
    draw.rounded_rectangle(bbox, radius=radius, fill=fill, outline=outline, width=width)

# -------------------------------------------------------------
# 1. СТРУКТУРНАЯ СХЕМА САЙТА (Древовидно-решётчатая)
# -------------------------------------------------------------
def generate_site_structure():
    w, h = 1600, 1000
    img = Image.new("RGB", (w, h), "#FFFFFF")
    draw = ImageDraw.Draw(img)

    f_title = get_font(22, bold=True)
    f_sub = get_font(12, bold=False)
    f_box_h = get_font(12, bold=True)
    f_box_t = get_font(10, bold=False)
    f_box_r = get_font(9.5, bold=True)

    # Шапка
    draw.rectangle([0, 0, w, 60], fill="#4A2C11")
    draw.text((w // 2, 30), "СТРУКТУРНАЯ СХЕМА СТРАНИЦ ВЕБ-СЕРВИСА «SWEETCRAFT» (ВАРИАНТ 1)", font=f_title, fill="#FFFFFF", anchor="mm")

    # Подзаголовок
    draw.text((60, 80), "Тип структуры: Древовидная с решётчатыми переходами (Иерархия каталога + сквозной конструктор и заказ)", font=f_sub, fill="#4B5563")

    # Легенда ролей (в правом верхнем углу)
    roles = [
        ("Гость (Все)", "#F3F4F6", "#4B5563"),
        ("Покупатель", "#FEF3C7", "#D97706"),
        ("Шеф-кондитер", "#E0E7FF", "#4F46E5"),
        ("Менеджер", "#DCFCE7", "#16A34A"),
        ("Администратор", "#FEE2E2", "#DC2626")
    ]
    rx = 850
    for r_title, r_bg, r_col in roles:
        draw_round_rect(draw, [rx, 75, rx + 130, 105], fill=r_bg, outline=r_col, width=1, radius=4)
        draw.text((rx + 65, 90), r_title, font=f_box_r, fill=r_col, anchor="mm")
        rx += 145

    # Узел 1: Главная (Уровень 0)
    root_x, root_y = w // 2 - 140, 130
    draw_round_rect(draw, [root_x, root_y, root_x + 280, root_y + 80], fill="#F3F4F6", outline="#4A2C11", width=2, radius=8)
    draw.text((w // 2, root_y + 24), "1. Главная страница (Витрина)", font=f_box_h, fill="#4A2C11", anchor="mm")
    draw.text((w // 2, root_y + 45), "URL: /", font=f_box_t, fill="#6B7280", anchor="mm")
    draw.text((w // 2, root_y + 64), "[Доступ: Гость, Покупатель]", font=f_box_r, fill="#4A2C11", anchor="mm")

    # Уровень 1 (4 ветки): Каталог, Конструктор, Личный кабинет, Служебный раздел
    branches = [
        {
            "title": "2. Каталог десертов", "url": "/catalog/", "role": "[Гость, Покупатель]", "bg": "#FEF3C7", "col": "#D97706", "x": 60, "y": 270,
            "children": [
                {"title": "Карточка десерта", "url": "/catalog/<slug>/", "role": "[Гость, Клиент]", "bg": "#FEF3C7", "col": "#D97706"},
                {"title": "Фильтры по коржу/начинке", "url": "/catalog/?crust=&filling=", "role": "[Все]", "bg": "#F3F4F6", "col": "#4B5563"},
                {"title": "Отзывы на десерт", "url": "/catalog/<slug>/reviews/", "role": "[Покупатель]", "bg": "#FEF3C7", "col": "#D97706"}
            ]
        },
        {
            "title": "3. Онлайн-конструктор", "url": "/builder/", "role": "[Особое требование]", "bg": "#FEF3C7", "col": "#B45309", "x": 440, "y": 270,
            "children": [
                {"title": "Выбор веса и ярусов", "url": "step=weight_tiers", "role": "[1-20 кг, 1-3 яруса]", "bg": "#FEF3C7", "col": "#B45309"},
                {"title": "Выбор коржа и начинки", "url": "step=crust_filling", "role": "[Базовые тарифы]", "bg": "#FEF3C7", "col": "#B45309"},
                {"title": "Декор и загрузка эскиза", "url": "step=decor_sketch", "role": "[Прикрепление файла]", "bg": "#FEF3C7", "col": "#B45309"},
                {"title": "Календарь лимита смены", "url": "api/check-date-capacity/", "role": "[Лимит 35/45 кг]", "bg": "#FEE2E2", "col": "#DC2626"}
            ]
        },
        {
            "title": "4. Корзина и Заказы", "url": "/checkout/", "role": "[Покупатель]", "bg": "#FEF3C7", "col": "#D97706", "x": 840, "y": 270,
            "children": [
                {"title": "Корзина покупок", "url": "/cart/", "role": "[Покупатель]", "bg": "#FEF3C7", "col": "#D97706"},
                {"title": "Оформление и предоплата", "url": "/checkout/", "role": "[Предоплата 30%]", "bg": "#FEF3C7", "col": "#D97706"},
                {"title": "Личный кабинет / Профиль", "url": "/profile/", "role": "[Покупатель]", "bg": "#FEF3C7", "col": "#D97706"},
                {"title": "Трекинг статуса заказа", "url": "/orders/<id>/", "role": "[Принят -> Выдан]", "bg": "#DCFCE7", "col": "#16A34A"}
            ]
        },
        {
            "title": "5. Производство и Админка", "url": "/dashboard/", "role": "[Персонал кондитерской]", "bg": "#E0E7FF", "col": "#4F46E5", "x": 1220, "y": 270,
            "children": [
                {"title": "Цех: Смены и лимиты веса", "url": "/confectioner/shifts/", "role": "[Кондитер]", "bg": "#E0E7FF", "col": "#4F46E5"},
                {"title": "Печать технологической карты", "url": "/orders/<id>/print/", "role": "[Кондитер]", "bg": "#E0E7FF", "col": "#4F46E5"},
                {"title": "Сводка заказов и экспорт CSV", "url": "/orders/export-csv/", "role": "[Менеджер]", "bg": "#DCFCE7", "col": "#16A34A"},
                {"title": "Системная панель Django", "url": "/admin/", "role": "[Администратор]", "bg": "#FEE2E2", "col": "#DC2626"}
            ]
        }
    ]

    # Линии от корня к 4 веткам
    draw.line([(w // 2, root_y + 80), (w // 2, 240)], fill="#4A2C11", width=2)
    draw.line([(220, 240), (1380, 240)], fill="#4A2C11", width=2)

    for b in branches:
        bx = b["x"]
        by = b["y"]
        center_x = bx + 160

        # Соединитель от горизонтали к ветке
        draw.line([(center_x, 240), (center_x, by)], fill="#4A2C11", width=2)

        # Карточка ветки 1 уровня
        draw_round_rect(draw, [bx, by, bx + 320, by + 75], fill=b["bg"], outline=b["col"], width=2, radius=8)
        draw.text((center_x, by + 22), b["title"], font=f_box_h, fill="#1F2937", anchor="mm")
        draw.text((center_x, by + 42), f"URL: {b['url']}", font=f_box_t, fill="#6B7280", anchor="mm")
        draw.text((center_x, by + 60), b["role"], font=f_box_r, fill=b["col"], anchor="mm")

        # Дочерние страницы 2 уровня
        cy_pos = by + 105
        for ch in b["children"]:
            draw.line([(center_x, cy_pos - 15), (center_x, cy_pos)], fill="#9CA3AF", width=1)
            draw_round_rect(draw, [bx + 15, cy_pos, bx + 305, cy_pos + 65], fill=ch["bg"], outline=ch["col"], width=1, radius=6)
            draw.text((center_x, cy_pos + 18), ch["title"], font=f_box_h, fill="#1F2937", anchor="mm")
            draw.text((center_x, cy_pos + 36), f"URL: {ch['url']}", font=f_box_t, fill="#4B5563", anchor="mm")
            draw.text((center_x, cy_pos + 52), ch["role"], font=f_box_r, fill=ch["col"], anchor="mm")
            cy_pos += 80

    # Решётчатые переходы (Cross-level links)
    draw.line([(380, 520), (440, 520)], fill="#D97706", width=2) # Из каталога в конструктор
    draw.text((410, 510), "➔", font=f_box_h, fill="#D97706", anchor="mm")

    draw.line([(760, 520), (840, 520)], fill="#D97706", width=2) # Из конструктора в корзину
    draw.text((800, 510), "➔", font=f_box_h, fill="#D97706", anchor="mm")

    out_png = OUT_DIR / "site_structure_day6.png"
    img.save(out_png, "PNG", quality=95)
    print(f"Saved site structure PNG: {out_png}")

    # Draw.io XML
    drawio_xml = """<mxfile host="Electron" modified="2026-11-17T21:00:00.000Z" agent="Antigravity" version="21.6.8" type="device">
  <diagram id="site_struct_sweetcraft" name="SweetCraft Site Structure">
    <mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" background="#ffffff">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="root1" value="1. Главная страница (Витрина)&#xa;URL: /&#xa;[Доступ: Гость, Покупатель]" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F3F4F6;strokeColor=#4A2C11;fontStyle=1;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="460" y="40" width="240" height="70" as="geometry" />
        </mxCell>
        <mxCell id="cat1" value="2. Каталог десертов&#xa;URL: /catalog/&#xa;[Гость, Покупатель]" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FEF3C7;strokeColor=#D97706;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="60" y="180" width="200" height="60" as="geometry" />
        </mxCell>
        <mxCell id="bld1" value="3. Онлайн-конструктор торта&#xa;URL: /builder/&#xa;[Особое требование Варианта 1]" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FEF3C7;strokeColor=#B45309;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="340" y="180" width="220" height="60" as="geometry" />
        </mxCell>
        <mxCell id="ord1" value="4. Корзина и Заказы&#xa;URL: /checkout/&#xa;[Покупатель]" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FEF3C7;strokeColor=#D97706;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="640" y="180" width="200" height="60" as="geometry" />
        </mxCell>
        <mxCell id="adm1" value="5. Цех и Управление&#xa;URL: /confectioner/shifts/&#xa;[Кондитер, Менеджер]" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E0E7FF;strokeColor=#4F46E5;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="920" y="180" width="200" height="60" as="geometry" />
        </mxCell>
        <mxCell id="e1" edge="1" parent="1" source="root1" target="cat1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#4A2C11;strokeWidth=2;">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e2" edge="1" parent="1" source="root1" target="bld1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#4A2C11;strokeWidth=2;">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e3" edge="1" parent="1" source="root1" target="ord1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#4A2C11;strokeWidth=2;">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="e4" edge="1" parent="1" source="root1" target="adm1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#4A2C11;strokeWidth=2;">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""
    out_drawio = OUT_DIR / "site_structure_day6.drawio"
    out_drawio.write_text(drawio_xml, encoding="utf-8")
    print(f"Saved site structure Draw.io: {out_drawio}")

# -------------------------------------------------------------
# 2. ТРИ СЦЕНАРИЯ ИСПОЛЬЗОВАНИЯ (USER FLOW С ВЕТВЛЕНИЯМИ И ОШИБКАМИ)
# -------------------------------------------------------------
def generate_user_flows():
    w, h = 1600, 1200
    img = Image.new("RGB", (w, h), "#FFFFFF")
    draw = ImageDraw.Draw(img)

    f_title = get_font(22, bold=True)
    f_flow_h = get_font(15, bold=True)
    f_node = get_font(11, bold=True)
    f_node_sub = get_font(9.5, bold=False)

    # Шапка
    draw.rectangle([0, 0, w, 60], fill="#1F2937")
    draw.text((w // 2, 30), "СЦЕНАРИИ ИСПОЛЬЗОВАНИЯ (USER FLOW) С ВЕТВЛЕНИЯМИ И ОШИБКАМИ", font=f_title, fill="#FFFFFF", anchor="mm")

    flows = [
        {
            "name": "Сценарий 1 (Покупатель): Конструирование авторского торта и проверка лимита цеха",
            "y": 80,
            "steps": [
                {"t": "Старт: Вход в конструктор", "desc": "Переход на /builder/", "type": "start", "col": "#4B5563", "bg": "#F3F4F6"},
                {"t": "Выбор параметров торта", "desc": "Вес (3.5 кг), бисквит, начинка", "type": "action", "col": "#B45309", "bg": "#FEF3C7"},
                {"t": "Авто-расчет цены (fetch)", "desc": "Формула Варианта 1", "type": "action", "col": "#B45309", "bg": "#FEF3C7"},
                {"t": "Выбор даты выдачи", "desc": "19 ноября 2026 г.", "type": "action", "col": "#B45309", "bg": "#FEF3C7"},
                {"t": "Проверка лимита цеха?", "desc": "Лимит: вес <= 35 кг/сут.", "type": "cond", "col": "#D97706", "bg": "#FEF3C7"},
                {"t": "[ОШИБКА]: Лимит исчерпан!", "desc": "Занято 35 из 35 кг (блокировка)", "type": "error", "col": "#DC2626", "bg": "#FEE2E2"},
                {"t": "Выбор свободной даты", "desc": "20 ноября (свободно 23 кг)", "type": "action", "col": "#16A34A", "bg": "#DCFCE7"},
                {"t": "Финиш: Оформление заказа", "desc": "Успешная запись в OrderItem", "type": "finish", "col": "#16A34A", "bg": "#DCFCE7"}
            ]
        },
        {
            "name": "Сценарий 2 (Гость -> Клиент): Поиск торта в каталоге и авторизация с ошибкой входа",
            "y": 440,
            "steps": [
                {"t": "Старт: Открытие каталога", "desc": "Переход на /catalog/", "type": "start", "col": "#4B5563", "bg": "#F3F4F6"},
                {"t": "Поиск и фильтрация", "desc": "Фильтр: 'Красный бархат'", "type": "action", "col": "#B45309", "bg": "#FEF3C7"},
                {"t": "Нажатие 'Купить'", "desc": "Запрос авторизации", "type": "action", "col": "#B45309", "bg": "#FEF3C7"},
                {"t": "Ввод логина и пароля", "desc": "Форма входа /login/", "type": "action", "col": "#B45309", "bg": "#FEF3C7"},
                {"t": "Пароль верный?", "desc": "Проверка auth хеша", "type": "cond", "col": "#D97706", "bg": "#FEF3C7"},
                {"t": "[ОШИБКА]: Неверный пароль", "desc": "Ошибка 'Пользователь не найден'", "type": "error", "col": "#DC2626", "bg": "#FEE2E2"},
                {"t": "Сброс/ввод корректного", "desc": "Успешный вход в систему", "type": "action", "col": "#16A34A", "bg": "#DCFCE7"},
                {"t": "Финиш: Товар в корзине", "desc": "Переход к /checkout/", "type": "finish", "col": "#16A34A", "bg": "#DCFCE7"}
            ]
        },
        {
            "name": "Сценарий 3 (Шеф-кондитер): Распределение заказов и контроль суточной загрузки смены",
            "y": 800,
            "steps": [
                {"t": "Старт: Вход шеф-кондитера", "desc": "Авторизация роли baker", "type": "start", "col": "#4B5563", "bg": "#F3F4F6"},
                {"t": "Календарь смен цеха", "desc": "Просмотр /confectioner/shifts/", "type": "action", "col": "#4F46E5", "bg": "#E0E7FF"},
                {"t": "Проверка наряда на дату", "desc": "Суммарный вес заказов", "type": "action", "col": "#4F46E5", "bg": "#E0E7FF"},
                {"t": "Заказ свыше лимита?", "desc": "Попытка добавить +10 кг сверх", "type": "cond", "col": "#D97706", "bg": "#FEF3C7"},
                {"t": "[ОШИБКА]: Перегруз цеха!", "desc": "Валидация CheckConstraint", "type": "error", "col": "#DC2626", "bg": "#FEE2E2"},
                {"t": "Смена статуса: 'В работе'", "desc": "Фиксация брони в транзакции", "type": "action", "col": "#16A34A", "bg": "#DCFCE7"},
                {"t": "Печать технологической карты", "desc": "Печатная форма /orders/<id>/print", "type": "finish", "col": "#16A34A", "bg": "#DCFCE7"}
            ]
        }
    ]

    for fl in flows:
        fy = fl["y"]
        draw.text((60, fy), fl["name"], font=f_flow_h, fill="#111827")

        # Рисуем узлы в 2 ряда или цепочкой
        nx = 60
        ny = fy + 36
        for idx, s in enumerate(fl["steps"]):
            # Рамка узла
            bw, bh = 170, 70
            is_error = s["type"] == "error"
            is_cond = s["type"] == "cond"
            border_w = 2 if (is_error or is_cond) else 1

            draw_round_rect(draw, [nx, ny, nx + bw, ny + bh], fill=s["bg"], outline=s["col"], width=border_w, radius=6)
            draw.text((nx + bw // 2, ny + 20), s["t"], font=f_node, fill=s["col"], anchor="mm")
            draw.text((nx + bw // 2, ny + 46), s["desc"], font=f_node_sub, fill="#4B5563", anchor="mm")

            # Стрелка к следующему узлу
            if idx < len(fl["steps"]) - 1:
                draw.line([(nx + bw, ny + bh // 2), (nx + bw + 20, ny + bh // 2)], fill="#9CA3AF", width=2)
                draw.polygon([(nx + bw + 20, ny + bh // 2), (nx + bw + 14, ny + bh // 2 - 4), (nx + bw + 14, ny + bh // 2 + 4)], fill="#9CA3AF")

            nx += bw + 24
            if nx + bw > w - 40 and idx < len(fl["steps"]) - 1:
                nx = 60
                ny += bh + 25

    out_png = OUT_DIR / "user_flows_day6.png"
    img.save(out_png, "PNG", quality=95)
    print(f"Saved user flows PNG: {out_png}")

    # Draw.io XML
    drawio_xml = """<mxfile host="Electron" modified="2026-11-17T21:00:00.000Z" agent="Antigravity" version="21.6.8" type="device">
  <diagram id="user_flows_sweetcraft" name="SweetCraft User Flows">
    <mxGraphModel dx="1422" dy="794" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" background="#ffffff">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="f1_start" value="1. Вход в конструктор&#xa;(/builder/)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F3F4F6;strokeColor=#4B5563;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="40" y="40" width="160" height="60" as="geometry" />
        </mxCell>
        <mxCell id="f1_pick" value="2. Выбор веса, бисквита,&#xa;начинки и декора" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FEF3C7;strokeColor=#B45309;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="240" y="40" width="170" height="60" as="geometry" />
        </mxCell>
        <mxCell id="f1_cond" value="3. Проверка суточного&#xa;лимита цеха на дату?" style="rhombus;whiteSpace=wrap;html=1;fillColor=#FEF3C7;strokeColor=#D97706;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="450" y="25" width="160" height="90" as="geometry" />
        </mxCell>
        <mxCell id="f1_err" value="[ОШИБКА]: Лимит исчерпан!&#xa;(Блокировка даты в календаре)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FEE2E2;strokeColor=#DC2626;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="450" y="160" width="160" height="60" as="geometry" />
        </mxCell>
        <mxCell id="f1_ok" value="4. Лимит в норме:&#xa;Оформление и предоплата" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#DCFCE7;strokeColor=#16A34A;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="660" y="40" width="170" height="60" as="geometry" />
        </mxCell>
        <mxCell id="e1_1" edge="1" parent="1" source="f1_start" target="f1_pick" style="strokeWidth=2;" />
        <mxCell id="e1_2" edge="1" parent="1" source="f1_pick" target="f1_cond" style="strokeWidth=2;" />
        <mxCell id="e1_3" edge="1" parent="1" source="f1_cond" target="f1_ok" style="strokeWidth=2;strokeColor=#16A34A;" value="Да (лимит OK)" />
        <mxCell id="e1_4" edge="1" parent="1" source="f1_cond" target="f1_err" style="strokeWidth=2;strokeColor=#DC2626;" value="Нет (перегруз)" />
        <mxCell id="e1_5" edge="1" parent="1" source="f1_err" target="f1_pick" style="strokeWidth=2;strokeColor=#DC2626;dashed=1;edgeStyle=orthogonalEdgeStyle;" value="Выбор другого дня" />
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""
    out_drawio = OUT_DIR / "user_flows_day6.drawio"
    out_drawio.write_text(drawio_xml, encoding="utf-8")
    print(f"Saved user flows Draw.io: {out_drawio}")

if __name__ == "__main__":
    generate_site_structure()
    generate_user_flows()
