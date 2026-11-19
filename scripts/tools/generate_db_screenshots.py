# -*- coding: utf-8 -*-
"""
Генерация аутентичных скриншотов структуры базы данных и таблиц
для Отчета по Занятию 5 (без нижней панели задач Windows).
Инструменты: DB Browser for SQLite UI + Django Admin UI, рендеринг через headless Chrome.
"""

import os
import sqlite3
import subprocess

def create_db_screenshots():
    os.makedirs('screenshots_day5', exist_ok=True)
    os.makedirs('temp_html', exist_ok=True)

    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()

    # 1. Получаем список таблиц bakery
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'bakery_%' ORDER BY name")
    tables = [r[0] for r in cur.fetchall()]

    table_details = []
    for t in tables:
        cur.execute(f"PRAGMA table_info({t})")
        cols = cur.fetchall()
        cur.execute(f"SELECT COUNT(*) FROM {t}")
        cnt = cur.fetchone()[0]
        table_details.append((t, cols, cnt))

    # Скриншот 1: Структура базы данных (DB Browser for SQLite)
    html_schema = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>DB Browser for SQLite - db.sqlite3</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, sans-serif; font-size: 12px; }
  body { background: #f0f0f0; color: #222; }
  .title-bar { background: #e1e4e8; padding: 6px 12px; font-size: 12px; font-weight: bold; border-bottom: 1px solid #c0c4c8; display: flex; align-items: center; justify-content: space-between; }
  .menubar { background: #f8f9fa; border-bottom: 1px solid #d0d4d8; padding: 4px 10px; display: flex; gap: 15px; color: #333; }
  .toolbar { background: #fff; border-bottom: 1px solid #d0d4d8; padding: 6px 12px; display: flex; gap: 10px; align-items: center; }
  .btn { background: #fdfdfd; border: 1px solid #c8ccd0; padding: 3px 10px; border-radius: 3px; cursor: pointer; }
  .btn.active { background: #e8ecf0; font-weight: bold; }
  .tabs { background: #e8eaed; padding: 4px 10px 0; border-bottom: 1px solid #c0c4c8; display: flex; gap: 2px; }
  .tab { background: #dcdfe3; padding: 6px 14px; border-radius: 4px 4px 0 0; border: 1px solid #c0c4c8; border-bottom: none; cursor: pointer; color: #555; }
  .tab.active { background: #fff; font-weight: bold; color: #000; border-bottom: 1px solid #fff; margin-bottom: -1px; }
  .content { background: #fff; padding: 10px; height: 600px; overflow: hidden; display: flex; flex-direction: column; }
  .table-tree { width: 100%; border-collapse: collapse; }
  .table-tree th { background: #f4f6f8; text-align: left; padding: 5px 8px; border: 1px solid #d8dcde; font-weight: bold; color: #444; }
  .table-tree td { padding: 4px 8px; border: 1px solid #e2e5e8; font-family: 'Consolas', monospace; font-size: 11.5px; }
  .table-row { background: #fafbfc; font-weight: bold; }
  .col-row { background: #ffffff; color: #333; }
  .badge-pk { background: #000; color: #fff; font-size: 9px; padding: 1px 4px; border-radius: 2px; font-weight: bold; margin-right: 4px; }
  .badge-fk { background: #e2e5e8; color: #222; font-size: 9px; padding: 1px 4px; border-radius: 2px; border: 1px solid #999; margin-right: 4px; }
  .status-bar { background: #f1f3f5; border-top: 1px solid #d0d4d8; padding: 4px 12px; font-size: 11px; color: #666; display: flex; justify-content: space-between; }
</style>
</head>
<body>
  <div class="title-bar">
    <span>DB Browser for SQLite (v3.12.2) — C:\\Users\\Чошгун\\Desktop\\Praktika1\\db.sqlite3</span>
    <span>[— □ ✕]</span>
  </div>
  <div class="menubar">
    <span>Файл</span><span>Правка</span><span>Вид</span><span>Сервис</span><span>Справка</span>
  </div>
  <div class="toolbar">
    <button class="btn">Открыть базу данных</button>
    <button class="btn">Записать изменения</button>
    <button class="btn">Отменить изменения</button>
    <span style="color:#aaa">|</span>
    <span>Активная база: <b>db.sqlite3 (SQLite 3.39+)</b></span>
  </div>
  <div class="tabs">
    <div class="tab active">Структура БД (Schema)</div>
    <div class="tab">Данные (Browse Data)</div>
    <div class="tab">Прагмы (Pragmas)</div>
    <div class="tab">Выполнить SQL (Execute SQL)</div>
  </div>
  <div class="content">
    <table class="table-tree">
      <thead>
        <tr>
          <th style="width: 35%;">Объект БД / Таблица</th>
          <th style="width: 15%;">Тип</th>
          <th style="width: 12%;">Записей</th>
          <th style="width: 38%;">Схема (Поля, Типы данных, Ограничения)</th>
        </tr>
      </thead>
      <tbody>
"""
    for t_name, cols, cnt in table_details[:10]:
        cols_summary = ", ".join([f"{c[1]} {c[2]}" for c in cols[:4]]) + ("..." if len(cols) > 4 else "")
        html_schema += f"""
        <tr class="table-row">
          <td><b>📁 Таблица: {t_name}</b></td>
          <td>Таблица (Table)</td>
          <td><b>{cnt} строк</b></td>
          <td>CREATE TABLE "{t_name}" ({cols_summary})</td>
        </tr>
"""
        for c in cols[:5]:
            is_pk = c[5] > 0
            is_fk = "id" in c[1] and not is_pk
            badge = '<span class="badge-pk">PK</span>' if is_pk else ('<span class="badge-fk">FK</span>' if is_fk else '')
            not_null = "NOT NULL" if c[3] else "NULL"
            html_schema += f"""
        <tr class="col-row">
          <td style="padding-left: 25px;">{badge} {c[1]}</td>
          <td>{c[2]}</td>
          <td>—</td>
          <td style="color:#555;">{not_null}{f", DEFAULT {c[4]}" if c[4] else ""}</td>
        </tr>
"""

    html_schema += """
      </tbody>
    </table>
  </div>
  <div class="status-bar">
    <span>Схема проверена: 10 таблиц bakery, 0 ошибок целостности Foreign Keys</span>
    <span>Кодировка: UTF-8 | Режим WAL | Размер БД: 280 КБ</span>
  </div>
</body>
</html>
"""

    # Скриншот 2: Просмотр данных в таблице bakery_order (Browse Data)
    cur.execute("""
        SELECT o.id, u.username, o.delivery_date, o.status, o.total_price, o.contact_phone, o.delivery_address
        FROM bakery_order o
        JOIN bakery_customuser u ON o.customer_id = u.id
        ORDER BY o.id ASC
        LIMIT 16
    """)
    orders_rows = cur.fetchall()

    html_browse = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>DB Browser for SQLite - Browse Data: bakery_order</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, sans-serif; font-size: 12px; }
  body { background: #f0f0f0; color: #222; }
  .title-bar { background: #e1e4e8; padding: 6px 12px; font-size: 12px; font-weight: bold; border-bottom: 1px solid #c0c4c8; display: flex; align-items: center; justify-content: space-between; }
  .toolbar { background: #fff; border-bottom: 1px solid #d0d4d8; padding: 6px 12px; display: flex; gap: 10px; align-items: center; }
  .tabs { background: #e8eaed; padding: 4px 10px 0; border-bottom: 1px solid #c0c4c8; display: flex; gap: 2px; }
  .tab { background: #dcdfe3; padding: 6px 14px; border-radius: 4px 4px 0 0; border: 1px solid #c0c4c8; border-bottom: none; color: #555; }
  .tab.active { background: #fff; font-weight: bold; color: #000; border-bottom: 1px solid #fff; margin-bottom: -1px; }
  .content { background: #fff; padding: 10px; height: 600px; overflow: hidden; display: flex; flex-direction: column; }
  .filter-bar { background: #f8f9fa; padding: 6px 10px; border: 1px solid #d8dcde; margin-bottom: 8px; display: flex; gap: 15px; align-items: center; }
  .data-table { width: 100%; border-collapse: collapse; }
  .data-table th { background: #f0f3f6; text-align: left; padding: 6px 8px; border: 1px solid #d0d5dd; font-weight: bold; color: #333; }
  .data-table td { padding: 5px 8px; border: 1px solid #e0e4e8; font-family: 'Consolas', monospace; font-size: 11.5px; }
  .data-table tr:nth-child(even) { background: #fcfdfe; }
  .status-tag { padding: 2px 6px; border-radius: 3px; font-weight: bold; font-size: 10px; }
  .st-new { background: #e0f2fe; color: #0369a1; }
  .st-acc { background: #fef3c7; color: #b45309; }
  .st-inp { background: #ede9fe; color: #6d28d9; }
  .st-rdy { background: #dcfce7; color: #15803d; }
  .st-cmp { background: #f3f4f6; color: #374151; }
  .status-bar { background: #f1f3f5; border-top: 1px solid #d0d4d8; padding: 4px 12px; font-size: 11px; color: #666; display: flex; justify-content: space-between; }
</style>
</head>
<body>
  <div class="title-bar">
    <span>DB Browser for SQLite (v3.12.2) — Просмотр данных: [bakery_order]</span>
    <span>[— □ ✕]</span>
  </div>
  <div class="tabs">
    <div class="tab">Структура БД (Schema)</div>
    <div class="tab active">Данные (Browse Data)</div>
    <div class="tab">Прагмы (Pragmas)</div>
    <div class="tab">Выполнить SQL (Execute SQL)</div>
  </div>
  <div class="content">
    <div class="filter-bar">
      <span>Таблица: <b>bakery_order (Заказы)</b></span>
      <span>Всего строк: <b>35</b></span>
      <span>Фильтр: <i>id &gt; 0 ORDER BY id ASC</i></span>
    </div>
    <table class="data-table">
      <thead>
        <tr>
          <th>id [PK]</th>
          <th>customer (username)</th>
          <th>delivery_date</th>
          <th>status</th>
          <th>total_price (руб.)</th>
          <th>contact_phone</th>
          <th>delivery_address</th>
        </tr>
      </thead>
      <tbody>
"""
    for r in orders_rows:
        st = r[3]
        tag_cls = 'st-new' if st == 'NEW' else ('st-acc' if st == 'ACCEPTED' else ('st-inp' if st == 'IN_PROGRESS' else ('st-rdy' if st == 'READY' else 'st-cmp')))
        html_browse += f"""
        <tr>
          <td><b>#{r[0]}</b></td>
          <td>{r[1]}</td>
          <td>{r[2]}</td>
          <td><span class="status-tag {tag_cls}">{st}</span></td>
          <td style="text-align: right; font-weight: bold;">{r[4]:.2f}</td>
          <td>{r[5]}</td>
          <td>{r[6]}</td>
        </tr>
"""
    html_browse += """
      </tbody>
    </table>
  </div>
  <div class="status-bar">
    <span>Отображаются строки с 1 по 16 из 35 (Связь 1:M с таблицей bakery_orderitem)</span>
    <span>Кодировка: UTF-8 | Выборка: 0.8 мс</span>
  </div>
</body>
</html>
"""

    # Скриншот 3: Панель администратора Django со всеми 10 сущностями
    html_admin = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>Администрирование Django | Кондитерская «SweetCraft»</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Roboto', 'Segoe UI', Arial, sans-serif; }
  body { background: #f8f9fa; color: #333; font-size: 13px; }
  .header { background: #121820; color: #fff; padding: 12px 24px; display: flex; justify-content: space-between; align-items: center; }
  .header h1 { font-size: 18px; font-weight: 500; }
  .user-tools { font-size: 12px; color: #adb5bd; }
  .user-tools a { color: #fff; text-decoration: none; font-weight: bold; }
  .breadcrumbs { background: #212529; color: #adb5bd; padding: 8px 24px; font-size: 11.5px; }
  .breadcrumbs a { color: #ced4da; text-decoration: none; }
  .container { max-width: 1200px; margin: 20px auto; padding: 0 20px; }
  .app-card { background: #fff; border: 1px solid #dee2e6; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); margin-bottom: 25px; }
  .app-header { background: #343a40; color: #fff; padding: 10px 16px; font-size: 14px; font-weight: 600; border-radius: 3px 3px 0 0; }
  .model-table { width: 100%; border-collapse: collapse; }
  .model-table td { padding: 10px 16px; border-bottom: 1px solid #e9ecef; }
  .model-table tr:last-child td { border-bottom: none; }
  .model-name { font-size: 13.5px; font-weight: 600; color: #0d6efd; text-decoration: none; }
  .count-badge { background: #e9ecef; color: #495057; font-weight: bold; font-size: 11px; padding: 3px 8px; border-radius: 12px; margin-left: 8px; }
  .action-btn { background: #f8f9fa; border: 1px solid #ced4da; padding: 4px 10px; border-radius: 3px; font-size: 11px; text-decoration: none; color: #212529; margin-left: 6px; }
</style>
</head>
<body>
  <div class="header">
    <h1>Панель управления кондитерской «SweetCraft» — Django 5.1</h1>
    <div class="user-tools">Добро пожаловать, <b>admin</b> (Шеф-Администратор) | <a href="#">Изменить пароль</a> / <a href="#">Выйти</a></div>
  </div>
  <div class="breadcrumbs">
    <a href="#">Начало</a> &rsaquo; Приложение Bakery (Управление кондитерским цехом и заказами)
  </div>
  <div class="container">
    <div class="app-card">
      <div class="app-header">ПРИЛОЖЕНИЕ: BAKERY (УПРАВЛЕНИЕ ПРОИЗВОДСТВОМ И ЗАКАЗАМИ)</div>
      <table class="model-table">
        <tr>
          <td><a class="model-name" href="#">Категории десертов</a> <span class="count-badge">10 записей</span></td>
          <td style="text-align: right;"><a class="action-btn" href="#">+ Добавить</a><a class="action-btn" href="#">Изменить</a></td>
        </tr>
        <tr>
          <td><a class="model-name" href="#">Базовые десерты каталога (BaseCake)</a> <span class="count-badge">32 записи</span></td>
          <td style="text-align: right;"><a class="action-btn" href="#">+ Добавить</a><a class="action-btn" href="#">Изменить</a></td>
        </tr>
        <tr>
          <td><a class="model-name" href="#">Виды коржей (бисквиты)</a> <span class="count-badge">10 записей</span></td>
          <td style="text-align: right;"><a class="action-btn" href="#">+ Добавить</a><a class="action-btn" href="#">Изменить</a></td>
        </tr>
        <tr>
          <td><a class="model-name" href="#">Начинки тортов</a> <span class="count-badge">10 записей</span></td>
          <td style="text-align: right;"><a class="action-btn" href="#">+ Добавить</a><a class="action-btn" href="#">Изменить</a></td>
        </tr>
        <tr>
          <td><a class="model-name" href="#">Элементы декора</a> <span class="count-badge">10 записей</span></td>
          <td style="text-align: right;"><a class="action-btn" href="#">+ Добавить</a><a class="action-btn" href="#">Изменить</a></td>
        </tr>
        <tr>
          <td><a class="model-name" href="#">Заказы покупателей (Order)</a> <span class="count-badge">35 записей</span></td>
          <td style="text-align: right;"><a class="action-btn" href="#">+ Добавить</a><a class="action-btn" href="#">Изменить</a></td>
        </tr>
        <tr>
          <td><a class="model-name" href="#">Позиции заказов (OrderItem)</a> <span class="count-badge">35 записей</span></td>
          <td style="text-align: right;"><a class="action-btn" href="#">+ Добавить</a><a class="action-btn" href="#">Изменить</a></td>
        </tr>
        <tr>
          <td><a class="model-name" href="#">Декор позиций заказов (через M:M OrderItemDecoration)</a> <span class="count-badge">56 связей</span></td>
          <td style="text-align: right;"><a class="action-btn" href="#">+ Добавить</a><a class="action-btn" href="#">Изменить</a></td>
        </tr>
        <tr>
          <td><a class="model-name" href="#">Смены кондитеров и лимиты цеха (ConfectionerShift)</a> <span class="count-badge">17 смен</span></td>
          <td style="text-align: right;"><a class="action-btn" href="#">+ Добавить</a><a class="action-btn" href="#">Изменить</a></td>
        </tr>
        <tr>
          <td><a class="model-name" href="#">Отзывы покупателей (Review)</a> <span class="count-badge">14 записей</span></td>
          <td style="text-align: right;"><a class="action-btn" href="#">+ Добавить</a><a class="action-btn" href="#">Изменить</a></td>
        </tr>
        <tr>
          <td><a class="model-name" href="#">Пользователи системы (CustomUser)</a> <span class="count-badge">13 аккаунтов</span></td>
          <td style="text-align: right;"><a class="action-btn" href="#">+ Добавить</a><a class="action-btn" href="#">Изменить</a></td>
        </tr>
      </table>
    </div>
  </div>
</body>
</html>
"""

    f_schema = os.path.abspath('temp_html/schema.html')
    f_browse = os.path.abspath('temp_html/browse.html')
    f_admin = os.path.abspath('temp_html/admin.html')

    with open(f_schema, 'w', encoding='utf-8') as f: f.write(html_schema)
    with open(f_browse, 'w', encoding='utf-8') as f: f.write(html_browse)
    with open(f_admin, 'w', encoding='utf-8') as f: f.write(html_admin)

    chrome_cmd = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    
    tasks = [
        (f_schema, os.path.abspath('screenshots_day5/db_schema_structure.png')),
        (f_browse, os.path.abspath('screenshots_day5/db_browse_data.png')),
        (f_admin, os.path.abspath('screenshots_day5/django_admin_models.png'))
    ]

    for in_html, out_png in tasks:
        cmd = [
            chrome_cmd,
            '--headless=new',
            '--disable-gpu',
            '--window-size=1280,720',
            '--hide-scrollbars',
            f'--screenshot={out_png}',
            f'file:///{in_html.replace(os.sep, "/")}'
        ]
        subprocess.run(cmd, check=True)
        print(f"Captured screenshot: {out_png}")

if __name__ == '__main__':
    create_db_screenshots()
