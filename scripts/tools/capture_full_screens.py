# -*- coding: utf-8 -*-
"""
Утилита для создания полноэкранных скриншотов веб-страниц «SweetCraft»
в двух обязательных разрешениях: Desktop 1440px и Mobile 375px.
Использует Chrome в headless-режиме: исключает любые элементы ОС Windows,
панель задач и окна других приложений.
"""

import os
import sys
import time
import subprocess
import threading
from pathlib import Path
from wsgiref.simple_server import make_server

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'confectionery_project.settings')

import django
django.setup()

from confectionery_project.wsgi import application

OUTPUT_DIR = BASE_DIR / "assets" / "screenshots" / "day7_9"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(CHROME_PATH):
    CHROME_PATH = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

PAGES = [
    ("home", "/"),
    ("catalog", "/catalog/"),
    ("cake_detail", "/cakes/cheesecake-caramel-pecan/"),
    ("builder", "/builder/?preview=1"),
    ("about", "/about/"),
    ("dashboard", "/dashboard/?preview=1"),
    ("orders", "/orders/?preview=1"),
    ("order_detail", "/orders/35/?preview=1"),
    ("profile", "/profile/?preview=1"),
    ("login", "/login/")
]

def run():
    print("=== Запуск локального тестового WSGI-сервера на 127.0.0.1:8000 ===")
    httpd = make_server('127.0.0.1', 8000, application)
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    time.sleep(1.5)

    print(f"Используем Chrome: {CHROME_PATH}")
    print(f"Каталог скриншотов: {OUTPUT_DIR}")

    resolutions = [
        ("desktop_1440", 1440, 950),
        ("mobile_375", 375, 812)
    ]

    for page_name, url_path in PAGES:
        target_url = f"http://127.0.0.1:8000{url_path}"
        for res_name, width, height in resolutions:
            out_file = OUTPUT_DIR / f"{res_name}_{page_name}.png"
            print(f"Снимок: {page_name:<12} [{width}x{height}] -> {out_file.name}")
            
            cmd = [
                CHROME_PATH,
                "--headless=new",
                "--disable-gpu",
                "--no-sandbox",
                f"--window-size={width},{height}",
                "--hide-scrollbars",
                f"--screenshot={str(out_file)}",
                target_url
            ]
            try:
                subprocess.run(cmd, check=True, timeout=15, capture_output=True)
            except Exception as e:
                print(f"  Ошибка при съемке {out_file.name}: {e}")

    httpd.shutdown()
    print("=== Съемка всех страниц в двух разрешениях завершена успешно! ===")

if __name__ == "__main__":
    run()
