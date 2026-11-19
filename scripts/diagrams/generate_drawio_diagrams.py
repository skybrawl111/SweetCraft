# -*- coding: utf-8 -*-
"""
Генерация файлов диаграмм в формате Draw.io (.drawio)
для открытия в app.diagrams.net или приложении draw.io
"""

import os
import xml.sax.saxutils as saxutils

def escape(val):
    return saxutils.escape(str(val))

def build_drawio_file(diagram_name, lanes, nodes, edges, width=1100, height=520):
    """
    lanes: list of dict(id, name, y, height, color)
    nodes: list of dict(id, parent, label, type, x, y, w, h)
      type in: 'start', 'end', 'task', 'gateway'
    edges: list of dict(id, source, target, label, waypoints)
    """
    xml = []
    xml.append('<mxfile host="app.diagrams.net" modified="2026-11-11T20:00:00.000Z" agent="5.0" version="21.0.0" type="device">')
    xml.append(f'  <diagram id="{diagram_name}" name="{diagram_name}">')
    xml.append(f'    <mxGraphModel dx="1200" dy="700" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{width}" pageHeight="{height}" background="#ffffff" math="0" shadow="0">')
    xml.append('      <root>')
    xml.append('        <mxCell id="0" />')
    xml.append('        <mxCell id="1" parent="0" />')

    # Add swimlanes
    for lane in lanes:
        lid = lane['id']
        name = escape(lane['name'])
        y = lane['y']
        h = lane['h']
        bg = lane.get('bg', '#F8F9FA')
        stroke = lane.get('stroke', '#4A5568')
        style = f"swimlane;html=1;horizontal=0;startSize=28;fillColor={bg};strokeColor={stroke};strokeWidth=1.5;fontFamily=Helvetica;fontSize=12;fontStyle=1;align=center;verticalAlign=middle;"
        xml.append(f'        <mxCell id="{lid}" value="{name}" style="{style}" vertex="1" parent="1">')
        xml.append(f'          <mxGeometry x="20" y="{y}" width="{width-40}" height="{h}" as="geometry" />')
        xml.append('        </mxCell>')

    # Add nodes
    for node in nodes:
        nid = node['id']
        label = escape(node['label'])
        ntype = node['type']
        pid = node.get('parent', '1')
        x = node['x']
        y = node['y']
        w = node['w']
        h = node['h']

        if ntype == 'start':
            style = "ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor=#D4EDDA;strokeColor=#28A745;strokeWidth=2;fontFamily=Helvetica;fontSize=10;fontStyle=1;align=center;"
        elif ntype == 'end':
            style = "ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor=#F8D7DA;strokeColor=#DC3545;strokeWidth=3;fontFamily=Helvetica;fontSize=10;fontStyle=1;align=center;"
        elif ntype == 'gateway':
            style = "rhombus;whiteSpace=wrap;html=1;fillColor=#FFF3CD;strokeColor=#856404;strokeWidth=1.5;fontFamily=Helvetica;fontSize=10;fontStyle=1;align=center;"
        else: # task
            bg = node.get('bg', '#E8F0FE')
            border = node.get('border', '#1A73E8')
            style = f"rounded=1;whiteSpace=wrap;html=1;fillColor={bg};strokeColor={border};strokeWidth=1.5;arcSize=10;fontFamily=Helvetica;fontSize=11;align=center;"

        xml.append(f'        <mxCell id="{nid}" value="{label}" style="{style}" vertex="1" parent="{pid}">')
        xml.append(f'          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />')
        xml.append('        </mxCell>')

    # Add edges
    for edge in edges:
        eid = edge['id']
        src = edge['source']
        tgt = edge['target']
        label = escape(edge.get('label', ''))
        style = "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#2D3748;strokeWidth=1.5;endArrow=block;endFill=1;fontFamily=Helvetica;fontSize=10;"
        xml.append(f'        <mxCell id="{eid}" value="{label}" style="{style}" edge="1" parent="1" source="{src}" target="{tgt}">')
        xml.append('          <mxGeometry relative="1" as="geometry" />')
        xml.append('        </mxCell>')

    xml.append('      </root>')
    xml.append('    </mxGraphModel>')
    xml.append('  </diagram>')
    xml.append('</mxfile>')

    return '\n'.join(xml)

def generate_all():
    out_dir = r"c:\Users\Чошгун\Desktop\Praktika1\diagrams"
    os.makedirs(out_dir, exist_ok=True)

    # 1. As-Is
    lanes_1 = [
        {'id': 'lane_cust', 'name': 'Клиент (Покупатель)', 'y': 30, 'h': 130, 'bg': '#F0FDF4'},
        {'id': 'lane_mgr', 'name': 'Менеджер по заказам', 'y': 160, 'h': 150, 'bg': '#EFF6FF'},
        {'id': 'lane_chef', 'name': 'Шеф-кондитер цеха', 'y': 310, 'h': 130, 'bg': '#FEF3C7'}
    ]
    nodes_1 = [
        {'id': 'start_1', 'parent': 'lane_cust', 'label': 'Потребность\nв торте', 'type': 'start', 'x': 50, 'y': 40, 'w': 50, 'h': 50},
        {'id': 'task_c1', 'parent': 'lane_cust', 'label': 'Написать сообщение\nв WhatsApp с фото', 'type': 'task', 'x': 130, 'y': 35, 'w': 130, 'h': 60},
        {'id': 'task_m1', 'parent': 'lane_mgr', 'label': 'Прочитать чат и\nзадать вопросы', 'type': 'task', 'x': 280, 'y': 40, 'w': 120, 'h': 60},
        {'id': 'task_c2', 'parent': 'lane_cust', 'label': 'Ответить на вопросы\nо весе и вкусе', 'type': 'task', 'x': 420, 'y': 35, 'w': 130, 'h': 60},
        {'id': 'task_m2', 'parent': 'lane_mgr', 'label': 'Рассчитать цену\nна калькуляторе', 'type': 'task', 'x': 570, 'y': 40, 'w': 120, 'h': 60},
        {'id': 'task_m3', 'parent': 'lane_mgr', 'label': 'Уточнить дату\nлично в цеху', 'type': 'task', 'x': 710, 'y': 40, 'w': 110, 'h': 60},
        {'id': 'task_k1', 'parent': 'lane_chef', 'label': 'Посмотреть записи\nв тетради смен', 'type': 'task', 'x': 710, 'y': 35, 'w': 120, 'h': 60},
        {'id': 'gw_agree', 'parent': 'lane_mgr', 'label': 'Клиент\nсогласен?', 'type': 'gateway', 'x': 840, 'y': 45, 'w': 50, 'h': 50},
        {'id': 'end_reject', 'parent': 'lane_mgr', 'label': 'Отказ\nиз-за цены', 'type': 'end', 'x': 840, 'y': 105, 'w': 40, 'h': 40},
        {'id': 'task_c3', 'parent': 'lane_cust', 'label': 'Перевести аванс\nпо номеру телефона', 'type': 'task', 'x': 910, 'y': 35, 'w': 120, 'h': 60},
        {'id': 'task_m4', 'parent': 'lane_mgr', 'label': 'Проверить чек\nи выписать стикер', 'type': 'task', 'x': 910, 'y': 40, 'w': 120, 'h': 60},
        {'id': 'end_1', 'parent': 'lane_chef', 'label': 'Заказ в цеху\nна стикере', 'type': 'end', 'x': 945, 'y': 40, 'w': 50, 'h': 50}
    ]
    edges_1 = [
        {'id': 'e1', 'source': 'start_1', 'target': 'task_c1'},
        {'id': 'e2', 'source': 'task_c1', 'target': 'task_m1'},
        {'id': 'e3', 'source': 'task_m1', 'target': 'task_c2'},
        {'id': 'e4', 'source': 'task_c2', 'target': 'task_m2'},
        {'id': 'e5', 'source': 'task_m2', 'target': 'task_m3'},
        {'id': 'e6', 'source': 'task_m3', 'target': 'task_k1'},
        {'id': 'e7', 'source': 'task_k1', 'target': 'gw_agree'},
        {'id': 'e8', 'source': 'gw_agree', 'target': 'end_reject', 'label': 'Нет'},
        {'id': 'e9', 'source': 'gw_agree', 'target': 'task_c3', 'label': 'Да'},
        {'id': 'e10', 'source': 'task_c3', 'target': 'task_m4'},
        {'id': 'e11', 'source': 'task_m4', 'target': 'end_1'}
    ]
    f1 = build_drawio_file('BPMN_Order_AsIs', lanes_1, nodes_1, edges_1, width=1100, height=480)
    with open(os.path.join(out_dir, "bpmn_order_as_is.drawio"), "w", encoding="utf-8") as f:
        f.write(f1)

    # 2. To-Be
    lanes_2 = [
        {'id': 'lane_c2', 'name': 'Покупатель (Клиент)', 'y': 30, 'h': 130, 'bg': '#F0FDF4'},
        {'id': 'lane_s2', 'name': 'Веб-сервис (Django)', 'y': 160, 'h': 150, 'bg': '#EFF6FF'},
        {'id': 'lane_k2', 'name': 'Кондитерский цех', 'y': 310, 'h': 130, 'bg': '#FEF3C7'}
    ]
    nodes_2 = [
        {'id': 'start_2', 'parent': 'lane_c2', 'label': 'Вход\nна сайт', 'type': 'start', 'x': 50, 'y': 40, 'w': 50, 'h': 50},
        {'id': 'task_2_c1', 'parent': 'lane_c2', 'label': 'Выбрать параметры\nи дату в конструкторе', 'type': 'task', 'x': 130, 'y': 35, 'w': 140, 'h': 60},
        {'id': 'task_2_s1', 'parent': 'lane_s2', 'label': 'Асинхронный расчет цены\nи проверка лимита (fetch)', 'type': 'task', 'x': 295, 'y': 40, 'w': 160, 'h': 60},
        {'id': 'gw_2_limit', 'parent': 'lane_s2', 'label': 'Лимит веса\nисчерпан?', 'type': 'gateway', 'x': 485, 'y': 45, 'w': 50, 'h': 50},
        {'id': 'task_2_c2', 'parent': 'lane_c2', 'label': 'Прикрепить эскиз\nи нажать «Заказать»', 'type': 'task', 'x': 570, 'y': 35, 'w': 140, 'h': 60},
        {'id': 'task_2_s2', 'parent': 'lane_s2', 'label': 'Запись в БД (atomic)\nи отправка email', 'type': 'task', 'x': 730, 'y': 40, 'w': 140, 'h': 60},
        {'id': 'task_2_k1', 'parent': 'lane_k2', 'label': 'Распечатать техкарту\nс эскизом в 1 клик', 'type': 'task', 'x': 890, 'y': 35, 'w': 140, 'h': 60},
        {'id': 'end_2', 'parent': 'lane_k2', 'label': 'Заказ в плане,\nвыпечка начата', 'type': 'end', 'x': 1050, 'y': 40, 'w': 50, 'h': 50}
    ]
    edges_2 = [
        {'id': 'e2_1', 'source': 'start_2', 'target': 'task_2_c1'},
        {'id': 'e2_2', 'source': 'task_2_c1', 'target': 'task_2_s1'},
        {'id': 'e2_3', 'source': 'task_2_s1', 'target': 'gw_2_limit'},
        {'id': 'e2_4', 'source': 'gw_2_limit', 'target': 'task_2_c1', 'label': 'Да (выбрать другую дату)'},
        {'id': 'e2_5', 'source': 'gw_2_limit', 'target': 'task_2_c2', 'label': 'Нет (лимит свободен)'},
        {'id': 'e2_6', 'source': 'task_2_c2', 'target': 'task_2_s2'},
        {'id': 'e2_7', 'source': 'task_2_s2', 'target': 'task_2_k1'},
        {'id': 'e2_8', 'source': 'task_2_k1', 'target': 'end_2'}
    ]
    f2 = build_drawio_file('BPMN_Order_ToBe', lanes_2, nodes_2, edges_2, width=1140, height=480)
    with open(os.path.join(out_dir, "bpmn_order_to_be.drawio"), "w", encoding="utf-8") as f:
        f.write(f2)

    # 3. Shift planning To-Be
    lanes_3 = [
        {'id': 'lane_sh_chef', 'name': 'Шеф-кондитер', 'y': 30, 'h': 140, 'bg': '#FEF3C7'},
        {'id': 'lane_sh_sys', 'name': 'Веб-сервис (Панель смен)', 'y': 170, 'h': 150, 'bg': '#EFF6FF'}
    ]
    nodes_3 = [
        {'id': 'start_3', 'parent': 'lane_sh_chef', 'label': 'Начало планового\nпериода смен', 'type': 'start', 'x': 50, 'y': 45, 'w': 50, 'h': 50},
        {'id': 'task_3_1', 'parent': 'lane_sh_chef', 'label': 'Авторизоваться\nв панели управления', 'type': 'task', 'x': 130, 'y': 40, 'w': 130, 'h': 60},
        {'id': 'task_3_2', 'parent': 'lane_sh_chef', 'label': 'Задать дату смены и\nлимит веса (кг)', 'type': 'task', 'x': 285, 'y': 40, 'w': 140, 'h': 60},
        {'id': 'task_3_3', 'parent': 'lane_sh_sys', 'label': 'Валидация квоты веса\n(35 кг / 45 кг)', 'type': 'task', 'x': 450, 'y': 45, 'w': 140, 'h': 60},
        {'id': 'gw_3', 'parent': 'lane_sh_sys', 'label': 'Данные\nкорректны?', 'type': 'gateway', 'x': 620, 'y': 50, 'w': 50, 'h': 50},
        {'id': 'task_3_4', 'parent': 'lane_sh_sys', 'label': 'Запись ConfectionerShift\nв базу данных', 'type': 'task', 'x': 700, 'y': 45, 'w': 150, 'h': 60},
        {'id': 'task_3_5', 'parent': 'lane_sh_sys', 'label': 'Обновление календаря\nна сайте для клиентов', 'type': 'task', 'x': 875, 'y': 45, 'w': 150, 'h': 60},
        {'id': 'end_3', 'parent': 'lane_sh_chef', 'label': 'Смены цеха\nутверждены', 'type': 'end', 'x': 925, 'y': 45, 'w': 50, 'h': 50}
    ]
    edges_3 = [
        {'id': 'e3_1', 'source': 'start_3', 'target': 'task_3_1'},
        {'id': 'e3_2', 'source': 'task_3_1', 'target': 'task_3_2'},
        {'id': 'e3_3', 'source': 'task_3_2', 'target': 'task_3_3'},
        {'id': 'e3_4', 'source': 'task_3_3', 'target': 'gw_3'},
        {'id': 'e3_5', 'source': 'gw_3', 'target': 'task_3_2', 'label': 'Нет (ошибка)'},
        {'id': 'e3_6', 'source': 'gw_3', 'target': 'task_3_4', 'label': 'Да'},
        {'id': 'e3_7', 'source': 'task_3_4', 'target': 'task_3_5'},
        {'id': 'e3_8', 'source': 'task_3_5', 'target': 'end_3'}
    ]
    f3 = build_drawio_file('BPMN_Shift_Planning_ToBe', lanes_3, nodes_3, edges_3, width=1060, height=360)
    with open(os.path.join(out_dir, "bpmn_shift_planning_to_be.drawio"), "w", encoding="utf-8") as f:
        f.write(f3)

    # 4. Fulfillment To-Be
    lanes_4 = [
        {'id': 'lane_f_chef', 'name': 'Кондитер / Зона выдачи', 'y': 30, 'h': 130, 'bg': '#FEF3C7'},
        {'id': 'lane_f_cust', 'name': 'Покупатель (Клиент)', 'y': 160, 'h': 140, 'bg': '#F0FDF4'},
        {'id': 'lane_f_sys', 'name': 'Веб-сервис (Django)', 'y': 300, 'h': 140, 'bg': '#EFF6FF'}
    ]
    nodes_4 = [
        {'id': 'start_4', 'parent': 'lane_f_chef', 'label': 'Торт готов\nи охлажден', 'type': 'start', 'x': 50, 'y': 40, 'w': 50, 'h': 50},
        {'id': 'task_4_1', 'parent': 'lane_f_chef', 'label': 'Сменить статус на\n«Готов к выдаче»', 'type': 'task', 'x': 130, 'y': 35, 'w': 140, 'h': 60},
        {'id': 'task_4_2', 'parent': 'lane_f_sys', 'label': 'Отправить email-уведомление\nо готовности торта', 'type': 'task', 'x': 295, 'y': 40, 'w': 160, 'h': 60},
        {'id': 'task_4_3', 'parent': 'lane_f_cust', 'label': 'Прийти в кондитерскую\nи принять заказ', 'type': 'task', 'x': 480, 'y': 40, 'w': 140, 'h': 60},
        {'id': 'task_4_4', 'parent': 'lane_f_chef', 'label': 'Выдать торт и перевести\nзаказ в «Выдан»', 'type': 'task', 'x': 645, 'y': 35, 'w': 150, 'h': 60},
        {'id': 'task_4_5', 'parent': 'lane_f_cust', 'label': 'Заполнить форму отзыва\nс оценкой (1-5 звезд)', 'type': 'task', 'x': 815, 'y': 40, 'w': 150, 'h': 60},
        {'id': 'task_4_6', 'parent': 'lane_f_sys', 'label': 'Опубликовать Review\nи обновить рейтинг', 'type': 'task', 'x': 980, 'y': 40, 'w': 140, 'h': 60},
        {'id': 'end_4', 'parent': 'lane_f_sys', 'label': 'Отзыв на сайте,\nзаказ закрыт', 'type': 'end', 'x': 1140, 'y': 45, 'w': 50, 'h': 50}
    ]
    edges_4 = [
        {'id': 'e4_1', 'source': 'start_4', 'target': 'task_4_1'},
        {'id': 'e4_2', 'source': 'task_4_1', 'target': 'task_4_2'},
        {'id': 'e4_3', 'source': 'task_4_2', 'target': 'task_4_3'},
        {'id': 'e4_4', 'source': 'task_4_3', 'target': 'task_4_4'},
        {'id': 'e4_5', 'source': 'task_4_4', 'target': 'task_4_5'},
        {'id': 'e4_6', 'source': 'task_4_5', 'target': 'task_4_6'},
        {'id': 'e4_7', 'source': 'task_4_6', 'target': 'end_4'}
    ]
    f4 = build_drawio_file('BPMN_Fulfillment_ToBe', lanes_4, nodes_4, edges_4, width=1220, height=480)
    with open(os.path.join(out_dir, "bpmn_order_fulfillment_to_be.drawio"), "w", encoding="utf-8") as f:
        f.write(f4)

    print("All 4 .drawio files created successfully in diagrams/!")

if __name__ == '__main__':
    generate_all()
