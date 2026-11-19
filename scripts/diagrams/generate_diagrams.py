# -*- coding: utf-8 -*-
"""
Генератор 4 BPMN-диаграмм для Занятия 2 (PNG + Draw.io / BPMN XML)
Вариант 1. «Заказ тортов и десертов в кондитерской»
"""

import os
from PIL import Image, ImageDraw, ImageFont

FONT_PATH = "C:/Windows/Fonts/arial.ttf"
FONT_BOLD_PATH = "C:/Windows/Fonts/arialbd.ttf"

font_title = ImageFont.truetype(FONT_BOLD_PATH, 16)
font_lane = ImageFont.truetype(FONT_BOLD_PATH, 14)
font_task = ImageFont.truetype(FONT_PATH, 12)
font_task_bold = ImageFont.truetype(FONT_BOLD_PATH, 12)
font_flow = ImageFont.truetype(FONT_BOLD_PATH, 11)
font_event = ImageFont.truetype(FONT_PATH, 11)

COLOR_BG = (255, 255, 255)
COLOR_POOL_BORDER = (70, 80, 95)
COLOR_LANE_BG = (248, 249, 251)
COLOR_LANE_HEADER = (235, 239, 245)
COLOR_TEXT = (35, 40, 50)
COLOR_TASK_BG = (255, 255, 255)
COLOR_TASK_BORDER = (30, 115, 190)
COLOR_TASK_AUTO_BG = (240, 247, 255)
COLOR_GATEWAY_BG = (255, 250, 235)
COLOR_GATEWAY_BORDER = (220, 150, 30)
COLOR_ARROW = (50, 60, 75)
COLOR_START = (76, 175, 80)
COLOR_END = (229, 57, 53)

def draw_rounded_rect(draw, coords, radius=8, fill=None, outline=None, width=2):
    x1, y1, x2, y2 = coords
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill, outline=outline, width=width)

def draw_diamond(draw, center, size, fill, outline, width=2):
    cx, cy = center
    s = size / 2
    points = [(cx, cy - s), (cx + s, cy), (cx, cy + s), (cx - s, cy)]
    draw.polygon(points, fill=fill, outline=outline)
    draw.line([(cx - s*0.35, cy - s*0.35), (cx + s*0.35, cy + s*0.35)], fill=outline, width=2)
    draw.line([(cx - s*0.35, cy + s*0.35), (cx + s*0.35, cy - s*0.35)], fill=outline, width=2)

def draw_circle(draw, center, radius, fill, outline, width=2):
    cx, cy = center
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=fill, outline=outline, width=width)

def draw_arrow(draw, points, color=COLOR_ARROW, width=2, label="", label_pos=None):
    for i in range(len(points) - 1):
        draw.line([points[i], points[i+1]], fill=color, width=width)
    p_last = points[-1]
    p_prev = points[-2]
    # Направление стрелки
    dx = p_last[0] - p_prev[0]
    dy = p_last[1] - p_prev[1]
    if dx > 0: # Вправо
        arrowhead = [(p_last[0], p_last[1]), (p_last[0] - 8, p_last[1] - 5), (p_last[0] - 8, p_last[1] + 5)]
    elif dx < 0: # Влево
        arrowhead = [(p_last[0], p_last[1]), (p_last[0] + 8, p_last[1] - 5), (p_last[0] + 8, p_last[1] + 5)]
    elif dy > 0: # Вниз
        arrowhead = [(p_last[0], p_last[1]), (p_last[0] - 5, p_last[1] - 8), (p_last[0] + 5, p_last[1] - 8)]
    else: # Вверх
        arrowhead = [(p_last[0], p_last[1]), (p_last[0] - 5, p_last[1] + 8), (p_last[0] + 5, p_last[1] + 8)]
    draw.polygon(arrowhead, fill=color)

    if label:
        lx, ly = label_pos if label_pos else ((p_prev[0] + p_last[0])//2, (p_prev[1] + p_last[1])//2 - 14)
        draw.text((lx, ly), label, fill=(160, 40, 40), font=font_flow)

def draw_multiline_text(draw, text, box, font=font_task, color=COLOR_TEXT):
    x1, y1, x2, y2 = box
    w_box = x2 - x1
    h_box = y2 - y1
    words = text.split()
    lines = []
    cur_line = []
    for word in words:
        test_line = " ".join(cur_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] < w_box - 12:
            cur_line.append(word)
        else:
            if cur_line:
                lines.append(" ".join(cur_line))
            cur_line = [word]
    if cur_line:
        lines.append(" ".join(cur_line))

    total_h = len(lines) * 15
    cur_y = y1 + (h_box - total_h) / 2
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        lw = bbox[2] - bbox[0]
        draw.text((x1 + (w_box - lw)/2, cur_y), line, fill=color, font=font)
        cur_y += 15

# =========================================================================
# ДИАГРАММА 1: Главный процесс As-Is («Прием и обработка заказа до автоматизации»)
# =========================================================================
def make_diagram_1_as_is():
    W, H = 1450, 680
    img = Image.new("RGB", (W, H), COLOR_BG)
    draw = ImageDraw.Draw(img)

    # Заголовок
    draw.text((30, 16), "Процесс 1 (As-Is): Прием и обработка заказа на торт до внедрения информационной системы", fill=COLOR_TEXT, font=font_title)

    pool_x = 30
    pool_y = 50
    pool_w = 1390
    lane_h = 190
    lanes = [
        "Клиент (Покупатель)",
        "Менеджер по приему заказов",
        "Шеф-кондитер цеха"
    ]

    # Отрисовка дорожек (Lanes)
    for i, lane_name in enumerate(lanes):
        ly = pool_y + i * lane_h
        draw.rectangle([pool_x, ly, pool_x + pool_w, ly + lane_h], outline=COLOR_POOL_BORDER, width=2)
        draw.rectangle([pool_x, ly, pool_x + 40, ly + lane_h], fill=COLOR_LANE_HEADER, outline=COLOR_POOL_BORDER, width=2)
        # Вертикальный текст дорожки
        txt_img = Image.new("RGBA", (lane_h, 38), (0,0,0,0))
        d_txt = ImageDraw.Draw(txt_img)
        d_txt.text((10, 8), lane_name, fill=COLOR_TEXT, font=font_lane)
        txt_rot = txt_img.rotate(90, expand=True)
        img.paste(txt_rot, (pool_x + 2, ly + (lane_h - txt_rot.height)//2), txt_rot)

    # Элементы дорожки 1: Клиент
    # Start Event
    draw_circle(draw, (110, pool_y + 95), 18, fill=(235, 250, 235), outline=COLOR_START, width=3)
    draw_multiline_text(draw, "Потребность\nв торте", (70, pool_y + 120, 150, pool_y + 160), font=font_event)

    # Task 1: Отправить запрос в WhatsApp
    draw_rounded_rect(draw, [180, pool_y + 65, 310, pool_y + 125], fill=COLOR_TASK_BG, outline=COLOR_TASK_BORDER)
    draw_multiline_text(draw, "Отправить запрос с фото в WhatsApp", [180, pool_y + 65, 310, pool_y + 125])

    # Task 3: Уточнить детали торта
    draw_rounded_rect(draw, [470, pool_y + 65, 590, pool_y + 125], fill=COLOR_TASK_BG, outline=COLOR_TASK_BORDER)
    draw_multiline_text(draw, "Ответить на вопросы о весе и дате", [470, pool_y + 65, 590, pool_y + 125])

    # Task 6: Перевести предоплату
    draw_rounded_rect(draw, [1040, pool_y + 65, 1170, pool_y + 125], fill=COLOR_TASK_BG, outline=COLOR_TASK_BORDER)
    draw_multiline_text(draw, "Перевести предоплату по номеру карты", [1040, pool_y + 65, 1170, pool_y + 125])

    # End Event (Отказ клиента по цене)
    draw_circle(draw, (980, pool_y + 40), 16, fill=(255, 235, 235), outline=COLOR_END, width=4)
    draw.text((945, pool_y + 18), "Отказ от цены", fill=COLOR_END, font=font_event)

    # Элементы дорожки 2: Менеджер
    # Task 2: Прочитать сообщение
    draw_rounded_rect(draw, [320, pool_y + lane_h + 65, 440, pool_y + lane_h + 125], fill=COLOR_TASK_BG, outline=COLOR_TASK_BORDER)
    draw_multiline_text(draw, "Прочитать сообщение и запросить детали", [320, pool_y + lane_h + 65, 440, pool_y + lane_h + 125])

    # Task 4: Рассчитать цену на калькуляторе
    draw_rounded_rect(draw, [530, pool_y + lane_h + 65, 650, pool_y + lane_h + 125], fill=COLOR_TASK_BG, outline=COLOR_TASK_BORDER)
    draw_multiline_text(draw, "Вручную рассчитать цену на калькуляторе", [530, pool_y + lane_h + 65, 650, pool_y + lane_h + 125])

    # Task 5: Сходить в цех
    draw_rounded_rect(draw, [680, pool_y + lane_h + 65, 790, pool_y + lane_h + 125], fill=COLOR_TASK_BG, outline=COLOR_TASK_BORDER)
    draw_multiline_text(draw, "Пойти в цех и спросить о загрузке", [680, pool_y + lane_h + 65, 790, pool_y + lane_h + 125])

    # Gateway: Клиент согласен с ценой?
    draw_diamond(draw, (980, pool_y + lane_h + 95), 44, fill=COLOR_GATEWAY_BG, outline=COLOR_GATEWAY_BORDER)
    draw.text((950, pool_y + lane_h + 130), "Согласен?", fill=COLOR_TEXT, font=font_event)

    # Task 7: Проверить поступление денег
    draw_rounded_rect(draw, [1180, pool_y + lane_h + 65, 1290, pool_y + lane_h + 125], fill=COLOR_TASK_BG, outline=COLOR_TASK_BORDER)
    draw_multiline_text(draw, "Проверить перевод в онлайн-банке", [1180, pool_y + lane_h + 65, 1290, pool_y + lane_h + 125])

    # Task 8: Записать заказ в журнал
    draw_rounded_rect(draw, [1305, pool_y + lane_h + 65, 1400, pool_y + lane_h + 125], fill=COLOR_TASK_BG, outline=COLOR_TASK_BORDER)
    draw_multiline_text(draw, "Записать в журнал и выписать стикер", [1305, pool_y + lane_h + 65, 1400, pool_y + lane_h + 125])

    # Элементы дорожки 3: Кондитер
    # Task: Проверить журнал смен
    draw_rounded_rect(draw, [760, pool_y + 2*lane_h + 65, 870, pool_y + 2*lane_h + 125], fill=COLOR_TASK_BG, outline=COLOR_TASK_BORDER)
    draw_multiline_text(draw, "Проверить записи в бумажном журнале", [760, pool_y + 2*lane_h + 65, 870, pool_y + 2*lane_h + 125])

    # Gateway: Успеем выпечь на дату?
    draw_diamond(draw, (910, pool_y + 2*lane_h + 95), 44, fill=COLOR_GATEWAY_BG, outline=COLOR_GATEWAY_BORDER)

    # End Event: Отказ из-за перегрузки
    draw_circle(draw, (910, pool_y + 2*lane_h + 165), 16, fill=(255, 235, 235), outline=COLOR_END, width=4)
    draw.text((860, pool_y + 2*lane_h + 172), "Отказ: цех полон", fill=COLOR_END, font=font_event)

    # End Event: Успех As-Is
    draw_circle(draw, (1350, pool_y + 2*lane_h + 95), 18, fill=(255, 235, 235), outline=COLOR_END, width=4)
    draw_multiline_text(draw, "Заказ на стикере\nв цеху", (1305, pool_y + 2*lane_h + 120, 1395, pool_y + 2*lane_h + 155), font=font_event)

    # Соединительные стрелки As-Is
    draw_arrow(draw, [(128, pool_y + 95), (180, pool_y + 95)])
    draw_arrow(draw, [(310, pool_y + 95), (380, pool_y + 95), (380, pool_y + lane_h + 65)])
    draw_arrow(draw, [(440, pool_y + lane_h + 95), (470, pool_y + lane_h + 95), (470, pool_y + 125), (470, pool_y + 95), (470, pool_y + 95)])
    draw_arrow(draw, [(440, pool_y + lane_h + 80), (500, pool_y + lane_h + 80), (500, pool_y + 125)])
    draw_arrow(draw, [(590, pool_y + 95), (610, pool_y + 95), (610, pool_y + lane_h + 65)])
    draw_arrow(draw, [(650, pool_y + lane_h + 95), (680, pool_y + lane_h + 95)])
    draw_arrow(draw, [(735, pool_y + lane_h + 125), (735, pool_y + 2*lane_h + 95), (760, pool_y + 2*lane_h + 95)])
    draw_arrow(draw, [(870, pool_y + 2*lane_h + 95), (888, pool_y + 2*lane_h + 95)])
    
    # Ветвление цеха
    draw_arrow(draw, [(910, pool_y + 2*lane_h + 117), (910, pool_y + 2*lane_h + 149)], label="[Перегруз]", label_pos=(915, pool_y + 2*lane_h + 125))
    draw_arrow(draw, [(932, pool_y + 2*lane_h + 95), (980, pool_y + 2*lane_h + 95), (980, pool_y + lane_h + 117)], label="[Свободно]", label_pos=(985, pool_y + 2*lane_h + 40))
    
    # Ветвление согласия
    draw_arrow(draw, [(980, pool_y + lane_h + 73), (980, pool_y + 56)], label="[Дорого]", label_pos=(985, pool_y + 70))
    draw_arrow(draw, [(1002, pool_y + lane_h + 95), (1030, pool_y + lane_h + 95), (1030, pool_y + 95), (1040, pool_y + 95)], label="[Согласен]", label_pos=(1005, pool_y + lane_h + 75))
    
    # Завершение
    draw_arrow(draw, [(1170, pool_y + 95), (1235, pool_y + 95), (1235, pool_y + lane_h + 65)])
    draw_arrow(draw, [(1290, pool_y + lane_h + 95), (1305, pool_y + lane_h + 95)])
    draw_arrow(draw, [(1350, pool_y + lane_h + 125), (1350, pool_y + 2*lane_h + 77)])

    img.save("assets/diagrams/bpmn_order_as_is.png")
    print("Saved assets/diagrams/bpmn_order_as_is.png")

# =========================================================================
# ДИАГРАММА 2: Главный процесс To-Be («Прием заказа после внедрения веб-сервиса»)
# =========================================================================
def make_diagram_2_to_be():
    W, H = 1450, 680
    img = Image.new("RGB", (W, H), COLOR_BG)
    draw = ImageDraw.Draw(img)

    draw.text((30, 16), "Процесс 1 (To-Be): Прием и обработка заказа на торт после внедрения веб-сервиса на Django", fill=COLOR_TEXT, font=font_title)

    pool_x = 30
    pool_y = 50
    pool_w = 1390
    lane_h = 190
    lanes = [
        "Клиент (Покупатель)",
        "Веб-сервис Django (Бэкенд)",
        "Шеф-кондитер цеха"
    ]

    for i, lane_name in enumerate(lanes):
        ly = pool_y + i * lane_h
        draw.rectangle([pool_x, ly, pool_x + pool_w, ly + lane_h], outline=COLOR_POOL_BORDER, width=2)
        draw.rectangle([pool_x, ly, pool_x + 40, ly + lane_h], fill=COLOR_LANE_HEADER, outline=COLOR_POOL_BORDER, width=2)
        txt_img = Image.new("RGBA", (lane_h, 38), (0,0,0,0))
        d_txt = ImageDraw.Draw(txt_img)
        d_txt.text((10, 8), lane_name, fill=COLOR_TEXT, font=font_lane)
        txt_rot = txt_img.rotate(90, expand=True)
        img.paste(txt_rot, (pool_x + 2, ly + (lane_h - txt_rot.height)//2), txt_rot)

    # Дорожка 1: Клиент
    # Start Event
    draw_circle(draw, (110, pool_y + 95), 18, fill=(235, 250, 235), outline=COLOR_START, width=3)
    draw_multiline_text(draw, "Потребность\nв заказе", (70, pool_y + 120, 150, pool_y + 160), font=font_event)

    # Task 1: Выбрать параметры в конструкторе
    draw_rounded_rect(draw, [180, pool_y + 65, 320, pool_y + 125], fill=COLOR_TASK_BG, outline=COLOR_TASK_BORDER)
    draw_multiline_text(draw, "Выбрать вес, начинку, корж и дату выдачи", [180, pool_y + 65, 320, pool_y + 125])

    # Task 3: Загрузить эскиз и оформить
    draw_rounded_rect(draw, [780, pool_y + 65, 920, pool_y + 125], fill=COLOR_TASK_BG, outline=COLOR_TASK_BORDER)
    draw_multiline_text(draw, "Загрузить эскиз (до 5 МБ) и нажать «Заказать»", [780, pool_y + 65, 920, pool_y + 125])

    # Дорожка 2: Веб-сервис Django
    # Task 2: Асинхронный расчет (Fetch)
    draw_rounded_rect(draw, [350, pool_y + lane_h + 65, 490, pool_y + lane_h + 125], fill=COLOR_TASK_AUTO_BG, outline=COLOR_TASK_BORDER)
    draw_multiline_text(draw, "Рассчитать цену и проверить лимит цеха (fetch)", [350, pool_y + lane_h + 65, 490, pool_y + lane_h + 125])

    # Gateway: Лимит смены превышен?
    draw_diamond(draw, (550, pool_y + lane_h + 95), 44, fill=COLOR_GATEWAY_BG, outline=COLOR_GATEWAY_BORDER)

    # Task: Вывести предупреждение
    draw_rounded_rect(draw, [480, pool_y + lane_h + 135, 620, pool_y + lane_h + 180], fill=(255, 240, 240), outline=COLOR_END)
    draw_multiline_text(draw, "Вывести сообщение о перегрузе смены", [480, pool_y + lane_h + 135, 620, pool_y + lane_h + 180])

    # Task: Отобразить цену и доступность
    draw_rounded_rect(draw, [640, pool_y + lane_h + 65, 760, pool_y + lane_h + 125], fill=COLOR_TASK_AUTO_BG, outline=COLOR_TASK_BORDER)
    draw_multiline_text(draw, "Отобразить расчетную цену и статус даты", [640, pool_y + lane_h + 65, 760, pool_y + lane_h + 125])

    # Task 4: Сохранить заказ в transaction.atomic
    draw_rounded_rect(draw, [950, pool_y + lane_h + 65, 1090, pool_y + lane_h + 125], fill=COLOR_TASK_AUTO_BG, outline=COLOR_TASK_BORDER)
    draw_multiline_text(draw, "Зафиксировать заказ в БД (transaction.atomic)", [950, pool_y + lane_h + 65, 1090, pool_y + lane_h + 125])

    # Task 5: Сгенерировать техкарту и отправить Email
    draw_rounded_rect(draw, [1120, pool_y + lane_h + 65, 1260, pool_y + lane_h + 125], fill=COLOR_TASK_AUTO_BG, outline=COLOR_TASK_BORDER)
    draw_multiline_text(draw, "Отправить Email клиенту и сформировать бланк", [1120, pool_y + lane_h + 65, 1260, pool_y + lane_h + 125])

    # Дорожка 3: Кондитер цеха
    # Task 6: Распечатать техкарту
    draw_rounded_rect(draw, [1120, pool_y + 2*lane_h + 65, 1260, pool_y + 2*lane_h + 125], fill=COLOR_TASK_BG, outline=COLOR_TASK_BORDER)
    draw_multiline_text(draw, "Распечатать техкарту и выпекать по рецептуре", [1120, pool_y + 2*lane_h + 65, 1260, pool_y + 2*lane_h + 125])

    # End Event
    draw_circle(draw, (1340, pool_y + 2*lane_h + 95), 18, fill=(235, 250, 235), outline=COLOR_START, width=4)
    draw_multiline_text(draw, "Заказ принят в цех\nс гарантией брони", (1290, pool_y + 2*lane_h + 120, 1390, pool_y + 2*lane_h + 155), font=font_event)

    # Стрелки To-Be
    draw_arrow(draw, [(128, pool_y + 95), (180, pool_y + 95)])
    draw_arrow(draw, [(320, pool_y + 95), (340, pool_y + 95), (340, pool_y + lane_h + 95), (350, pool_y + lane_h + 95)])
    draw_arrow(draw, [(490, pool_y + lane_h + 95), (528, pool_y + lane_h + 95)])

    # Ветвление шлюза
    draw_arrow(draw, [(550, pool_y + lane_h + 117), (550, pool_y + lane_h + 135)], label="[Превышен]", label_pos=(555, pool_y + lane_h + 118))
    draw_arrow(draw, [(480, pool_y + lane_h + 157), (250, pool_y + lane_h + 157), (250, pool_y + 125)])
    draw_arrow(draw, [(572, pool_y + lane_h + 95), (640, pool_y + lane_h + 95)], label="[Свободно]", label_pos=(575, pool_y + lane_h + 78))

    draw_arrow(draw, [(760, pool_y + lane_h + 95), (770, pool_y + lane_h + 95), (770, pool_y + 95), (780, pool_y + 95)])
    draw_arrow(draw, [(920, pool_y + 95), (935, pool_y + 95), (935, pool_y + lane_h + 95), (950, pool_y + lane_h + 95)])
    draw_arrow(draw, [(1090, pool_y + lane_h + 95), (1120, pool_y + lane_h + 95)])
    draw_arrow(draw, [(1190, pool_y + lane_h + 125), (1190, pool_y + 2*lane_h + 65)])
    draw_arrow(draw, [(1260, pool_y + 2*lane_h + 95), (1322, pool_y + 2*lane_h + 95)])

    img.save("assets/diagrams/bpmn_order_to_be.png")
    print("Saved assets/diagrams/bpmn_order_to_be.png")

# =========================================================================
# ДИАГРАММА 3: Процесс 2 To-Be («Планирование смен и суточных лимитов»)
# =========================================================================
def make_diagram_3_shift_planning():
    W, H = 1350, 520
    img = Image.new("RGB", (W, H), COLOR_BG)
    draw = ImageDraw.Draw(img)

    draw.text((30, 16), "Процесс 2: Планирование смен цеха и установка суточных лимитов выпечки (Особое требование)", fill=COLOR_TEXT, font=font_title)

    pool_x = 30
    pool_y = 50
    pool_w = 1290
    lane_h = 210
    lanes = [
        "Шеф-кондитер / Управляющий цеха",
        "Веб-сервис Django (Бэкенд)"
    ]

    for i, lane_name in enumerate(lanes):
        ly = pool_y + i * lane_h
        draw.rectangle([pool_x, ly, pool_x + pool_w, ly + lane_h], outline=COLOR_POOL_BORDER, width=2)
        draw.rectangle([pool_x, ly, pool_x + 40, ly + lane_h], fill=COLOR_LANE_HEADER, outline=COLOR_POOL_BORDER, width=2)
        txt_img = Image.new("RGBA", (lane_h, 38), (0,0,0,0))
        d_txt = ImageDraw.Draw(txt_img)
        d_txt.text((10, 8), lane_name, fill=COLOR_TEXT, font=font_lane)
        txt_rot = txt_img.rotate(90, expand=True)
        img.paste(txt_rot, (pool_x + 2, ly + (lane_h - txt_rot.height)//2), txt_rot)

    # Дорожка 1: Шеф-кондитер
    draw_circle(draw, (110, pool_y + 105), 18, fill=(235, 250, 235), outline=COLOR_START, width=3)
    draw_multiline_text(draw, "Период\nпланирования", (70, pool_y + 130, 150, pool_y + 170), font=font_event)

    # Task 1
    draw_rounded_rect(draw, [180, pool_y + 75, 320, pool_y + 135], fill=COLOR_TASK_BG, outline=COLOR_TASK_BORDER)
    draw_multiline_text(draw, "Открыть панель смен в админ-разделе", [180, pool_y + 75, 320, pool_y + 135])

    # Task 2
    draw_rounded_rect(draw, [360, pool_y + 75, 490, pool_y + 135], fill=COLOR_TASK_BG, outline=COLOR_TASK_BORDER)
    draw_multiline_text(draw, "Выбрать дату смены и дежурного кондитера", [360, pool_y + 75, 490, pool_y + 135])

    # Gateway
    draw_diamond(draw, (560, pool_y + 105), 44, fill=COLOR_GATEWAY_BG, outline=COLOR_GATEWAY_BORDER)

    # Task 3a
    draw_rounded_rect(draw, [650, pool_y + 50, 800, pool_y + 105], fill=COLOR_TASK_BG, outline=COLOR_TASK_BORDER)
    draw_multiline_text(draw, "Установить повышенный лимит (45 кг)", [650, pool_y + 50, 800, pool_y + 105])

    # Task 3b
    draw_rounded_rect(draw, [650, pool_y + 125, 800, pool_y + 180], fill=COLOR_TASK_BG, outline=COLOR_TASK_BORDER)
    draw_multiline_text(draw, "Установить стандартный лимит (35 кг)", [650, pool_y + 125, 800, pool_y + 180])

    # Task 4
    draw_rounded_rect(draw, [840, pool_y + 75, 960, pool_y + 135], fill=COLOR_TASK_BG, outline=COLOR_TASK_BORDER)
    draw_multiline_text(draw, "Нажать «Сохранить смену»", [840, pool_y + 75, 960, pool_y + 135])

    # Дорожка 2: Веб-сервис
    # Task 5
    draw_rounded_rect(draw, [840, pool_y + lane_h + 75, 990, pool_y + lane_h + 135], fill=COLOR_TASK_AUTO_BG, outline=COLOR_TASK_BORDER)
    draw_multiline_text(draw, "Записать смену ConfectionerShift в БД", [840, pool_y + lane_h + 75, 990, pool_y + lane_h + 135])

    # Task 6
    draw_rounded_rect(draw, [1040, pool_y + lane_h + 75, 1180, pool_y + lane_h + 135], fill=COLOR_TASK_AUTO_BG, outline=COLOR_TASK_BORDER)
    draw_multiline_text(draw, "Обновить доступные квоты в конструкторе", [1040, pool_y + lane_h + 75, 1180, pool_y + lane_h + 135])

    # End Event
    draw_circle(draw, (1240, pool_y + lane_h + 105), 18, fill=(235, 250, 235), outline=COLOR_START, width=4)
    draw_multiline_text(draw, "Лимиты смен\nактуальны", (1200, pool_y + lane_h + 130, 1280, pool_y + lane_h + 170), font=font_event)

    # Стрелки
    draw_arrow(draw, [(128, pool_y + 105), (180, pool_y + 105)])
    draw_arrow(draw, [(320, pool_y + 105), (360, pool_y + 105)])
    draw_arrow(draw, [(490, pool_y + 105), (538, pool_y + 105)])

    draw_arrow(draw, [(560, pool_y + 83), (560, pool_y + 77), (650, pool_y + 77)], label="[Праздник/Выходной]", label_pos=(540, pool_y + 40))
    draw_arrow(draw, [(560, pool_y + 127), (560, pool_y + 152), (650, pool_y + 152)], label="[Будний день]", label_pos=(550, pool_y + 160))

    draw_arrow(draw, [(800, pool_y + 77), (820, pool_y + 77), (820, pool_y + 105), (840, pool_y + 105)])
    draw_arrow(draw, [(800, pool_y + 152), (820, pool_y + 152), (820, pool_y + 105), (840, pool_y + 105)])

    draw_arrow(draw, [(900, pool_y + 135), (900, pool_y + lane_h + 75)])
    draw_arrow(draw, [(990, pool_y + lane_h + 105), (1040, pool_y + lane_h + 105)])
    draw_arrow(draw, [(1180, pool_y + lane_h + 105), (1222, pool_y + lane_h + 105)])

    img.save("assets/diagrams/bpmn_shift_planning_to_be.png")
    print("Saved assets/diagrams/bpmn_shift_planning_to_be.png")

# =========================================================================
# ДИАГРАММА 4: Процесс 3 To-Be («Выдача готового изделия и сбор отзывов»)
# =========================================================================
def make_diagram_4_fulfillment():
    W, H = 1450, 680
    img = Image.new("RGB", (W, H), COLOR_BG)
    draw = ImageDraw.Draw(img)

    draw.text((30, 16), "Процесс 3: Выдача готового десерта клиенту и сбор обратной связи (CRUD отзывов)", fill=COLOR_TEXT, font=font_title)

    pool_x = 30
    pool_y = 50
    pool_w = 1390
    lane_h = 190
    lanes = [
        "Кондитер цеха (Мастер)",
        "Клиент (Покупатель)",
        "Веб-сервис Django (Бэкенд)"
    ]

    for i, lane_name in enumerate(lanes):
        ly = pool_y + i * lane_h
        draw.rectangle([pool_x, ly, pool_x + pool_w, ly + lane_h], outline=COLOR_POOL_BORDER, width=2)
        draw.rectangle([pool_x, ly, pool_x + 40, ly + lane_h], fill=COLOR_LANE_HEADER, outline=COLOR_POOL_BORDER, width=2)
        txt_img = Image.new("RGBA", (lane_h, 38), (0,0,0,0))
        d_txt = ImageDraw.Draw(txt_img)
        d_txt.text((10, 8), lane_name, fill=COLOR_TEXT, font=font_lane)
        txt_rot = txt_img.rotate(90, expand=True)
        img.paste(txt_rot, (pool_x + 2, ly + (lane_h - txt_rot.height)//2), txt_rot)

    # Дорожка 1: Кондитер
    draw_circle(draw, (110, pool_y + 95), 18, fill=(235, 250, 235), outline=COLOR_START, width=3)
    draw_multiline_text(draw, "Торт готов\nи охлажден", (70, pool_y + 120, 150, pool_y + 160), font=font_event)

    # Task 1
    draw_rounded_rect(draw, [180, pool_y + 65, 320, pool_y + 125], fill=COLOR_TASK_BG, outline=COLOR_TASK_BORDER)
    draw_multiline_text(draw, "Упаковать торт и перевести статус в «Готов к выдаче»", [180, pool_y + 65, 320, pool_y + 125])

    # Task 4
    draw_rounded_rect(draw, [620, pool_y + 65, 750, pool_y + 125], fill=COLOR_TASK_BG, outline=COLOR_TASK_BORDER)
    draw_multiline_text(draw, "Сверить номер заказа и выдать торт клиенту", [620, pool_y + 65, 750, pool_y + 125])

    # Task 5
    draw_rounded_rect(draw, [780, pool_y + 65, 910, pool_y + 125], fill=COLOR_TASK_BG, outline=COLOR_TASK_BORDER)
    draw_multiline_text(draw, "Изменить статус заказа на «Выдан клиенту»", [780, pool_y + 65, 910, pool_y + 125])

    # Дорожка 2: Клиент
    # Task 3
    draw_rounded_rect(draw, [470, pool_y + lane_h + 65, 590, pool_y + lane_h + 125], fill=COLOR_TASK_BG, outline=COLOR_TASK_BORDER)
    draw_multiline_text(draw, "Прибыть в пункт выдачи кондитерской", [470, pool_y + lane_h + 65, 590, pool_y + lane_h + 125])

    # Gateway: Желает оставить отзыв?
    draw_diamond(draw, (1020, pool_y + lane_h + 95), 44, fill=COLOR_GATEWAY_BG, outline=COLOR_GATEWAY_BORDER)

    # Task 6: Заполнить форму отзыва
    draw_rounded_rect(draw, [1120, pool_y + lane_h + 65, 1260, pool_y + lane_h + 125], fill=COLOR_TASK_BG, outline=COLOR_TASK_BORDER)
    draw_multiline_text(draw, "Поставить оценку и написать отзыв на сайте", [1120, pool_y + lane_h + 65, 1260, pool_y + lane_h + 125])

    # End Event (Без отзыва)
    draw_circle(draw, (1020, pool_y + lane_h + 165), 16, fill=(245, 245, 245), outline=(120, 120, 120), width=3)
    draw.text((965, pool_y + lane_h + 172), "Заказ закрыт без отзыва", fill=COLOR_TEXT, font=font_event)

    # Дорожка 3: Веб-сервис
    # Task 2
    draw_rounded_rect(draw, [340, pool_y + 2*lane_h + 65, 480, pool_y + 2*lane_h + 125], fill=COLOR_TASK_AUTO_BG, outline=COLOR_TASK_BORDER)
    draw_multiline_text(draw, "Отправить клиенту email-уведомление о готовности", [340, pool_y + 2*lane_h + 65, 480, pool_y + 2*lane_h + 125])

    # Task 7
    draw_rounded_rect(draw, [1120, pool_y + 2*lane_h + 65, 1260, pool_y + 2*lane_h + 125], fill=COLOR_TASK_AUTO_BG, outline=COLOR_TASK_BORDER)
    draw_multiline_text(draw, "Сохранить Review в БД и опубликовать в каталоге", [1120, pool_y + 2*lane_h + 65, 1260, pool_y + 2*lane_h + 125])

    # End Event (Успех)
    draw_circle(draw, (1350, pool_y + 2*lane_h + 95), 18, fill=(235, 250, 235), outline=COLOR_START, width=4)
    draw_multiline_text(draw, "Заказ завершен\nи оценен", (1305, pool_y + 2*lane_h + 120, 1395, pool_y + 2*lane_h + 155), font=font_event)

    # Стрелки
    draw_arrow(draw, [(128, pool_y + 95), (180, pool_y + 95)])
    draw_arrow(draw, [(320, pool_y + 95), (330, pool_y + 95), (330, pool_y + 2*lane_h + 95), (340, pool_y + 2*lane_h + 95)])
    draw_arrow(draw, [(480, pool_y + 2*lane_h + 95), (530, pool_y + 2*lane_h + 95), (530, pool_y + lane_h + 125)])
    draw_arrow(draw, [(590, pool_y + lane_h + 95), (610, pool_y + lane_h + 95), (610, pool_y + 95), (620, pool_y + 95)])
    draw_arrow(draw, [(750, pool_y + 95), (780, pool_y + 95)])
    draw_arrow(draw, [(910, pool_y + 95), (960, pool_y + 95), (960, pool_y + lane_h + 95), (998, pool_y + lane_h + 95)])

    # Ветвление отзыва
    draw_arrow(draw, [(1020, pool_y + lane_h + 117), (1020, pool_y + lane_h + 149)], label="[Нет]", label_pos=(1025, pool_y + lane_h + 125))
    draw_arrow(draw, [(1042, pool_y + lane_h + 95), (1120, pool_y + lane_h + 95)], label="[Да, оставить]", label_pos=(1045, pool_y + lane_h + 75))

    draw_arrow(draw, [(1190, pool_y + lane_h + 125), (1190, pool_y + 2*lane_h + 65)])
    draw_arrow(draw, [(1260, pool_y + 2*lane_h + 95), (1332, pool_y + 2*lane_h + 95)])

    img.save("assets/diagrams/bpmn_order_fulfillment_to_be.png")
    print("Saved assets/diagrams/bpmn_order_fulfillment_to_be.png")

if __name__ == "__main__":
    make_diagram_1_as_is()
    make_diagram_2_to_be()
    make_diagram_3_shift_planning()
    make_diagram_4_fulfillment()
    print("All 4 BPMN diagrams generated successfully in PNG!")
