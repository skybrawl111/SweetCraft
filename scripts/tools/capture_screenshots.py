# -*- coding: utf-8 -*-
"""
Скрипт захвата скриншотов 10 сайтов-аналогов для Занятия 3.
Запускает Chrome headless без интерфейса ОС (без нижней панели задач).
Каждый скриншот проверяется и кадрируется через Pillow.
"""

import os
import time
import subprocess
from PIL import Image

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
OUT_DIR = r"c:\Users\Чошгун\Desktop\Praktika1\screenshots_day3"
os.makedirs(OUT_DIR, exist_ok=True)

SITES = [
    {
        "id": "1",
        "name": "agzamov.com",
        "main_url": "https://agzamov.com/",
        "inner_url": "https://agzamov.com/catalog/svadebnye/",
        "main_img": "site_1_main.png",
        "inner_img": "site_1_inner.png",
        "inner_desc": "Каталог свадебных авторских тортов"
    },
    {
        "id": "2",
        "name": "tortikannuchka.com",
        "main_url": "https://tortikannuchka.com/",
        "inner_url": "https://tortikannuchka.com/cakes",
        "main_img": "site_2_main.png",
        "inner_img": "site_2_inner.png",
        "inner_desc": "Витрина дизайнерских тортов"
    },
    {
        "id": "3",
        "name": "teabakery.ru",
        "main_url": "https://teabakery.ru/",
        "inner_url": "https://teabakery.ru/catalog/torty/",
        "main_img": "site_3_main.png",
        "inner_img": "site_3_inner.png",
        "inner_desc": "Каталог праздничных и бенто-тортов"
    },
    {
        "id": "4",
        "name": "british-bakery.ru",
        "main_url": "https://british-bakery.ru/",
        "inner_url": "https://british-bakery.ru/catalog/torty/",
        "main_img": "site_4_main.png",
        "inner_img": "site_4_inner.png",
        "inner_desc": "Каталог заказных десертов"
    },
    {
        "id": "5",
        "name": "cake-time.ru",
        "main_url": "https://cake-time.ru/",
        "inner_url": "https://cake-time.ru/catalog/",
        "main_img": "site_5_main.png",
        "inner_img": "site_5_inner.png",
        "inner_desc": "Каталог начинок и тортов"
    },
    {
        "id": "6",
        "name": "tortnadom.com",
        "main_url": "https://tortnadom.com/",
        "inner_url": "https://tortnadom.com/catalog/torty-na-zakaz/",
        "main_img": "site_6_main.png",
        "inner_img": "site_6_inner.png",
        "inner_desc": "Форма подбора и заказа торта"
    },
    {
        "id": "7",
        "name": "irisdelicia.ru",
        "main_url": "https://irisdelicia.ru/",
        "inner_url": "https://irisdelicia.ru/catalog/",
        "main_img": "site_7_main.png",
        "inner_img": "site_7_inner.png",
        "inner_desc": "Каталог заказных тортов"
    },
    {
        "id": "8",
        "name": "napoleoncake.ru",
        "main_url": "https://napoleoncake.ru/",
        "inner_url": "https://napoleoncake.ru/catalog/",
        "main_img": "site_8_main.png",
        "inner_img": "site_8_inner.png",
        "inner_desc": "Каталог авторских тортов Наполеон"
    },
    {
        "id": "9",
        "name": "magnoliabakery.com",
        "main_url": "https://www.magnoliabakery.com/",
        "inner_url": "https://www.magnoliabakery.com/collections/cakes",
        "main_img": "site_9_main.png",
        "inner_img": "site_9_inner.png",
        "inner_desc": "Каталог celebration cakes (США)"
    },
    {
        "id": "10",
        "name": "lolascupcakes.co.uk",
        "main_url": "https://www.lolascupcakes.co.uk/",
        "inner_url": "https://www.lolascupcakes.co.uk/pages/custom-cakes",
        "main_img": "site_10_main.png",
        "inner_img": "site_10_inner.png",
        "inner_desc": "Конструктор кастомных тортов (Великобритания)"
    }
]

def capture_url(url, out_path, is_mobile=False):
    win_size = "390,844" if is_mobile else "1280,820"
    user_agent = (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 "
        "(KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
        if is_mobile else
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )

    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        f"--window-size={win_size}",
        f"--user-agent={user_agent}",
        "--virtual-time-budget=5000",
        f"--screenshot={out_path}",
        url
    ]

    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=25)
        if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
            # Crop to guarantee no taskbar or border artifact
            with Image.open(out_path) as im:
                w, h = im.size
                # If desktop, crop top browser bar or bottom border if any
                cropped = im.crop((0, 0, w, h - 20 if h > 600 else h))
                cropped.save(out_path, optimize=True)
            print(f"OK: {url} -> {os.path.basename(out_path)}")
            return True
        else:
            print(f"FAIL (no file): {url}")
            return False
    except Exception as e:
        print(f"ERROR: {url} -> {e}")
        return False

def main():
    print("Starting screenshot capture for 10 websites...")
    results = {}
    for site in SITES:
        print(f"\nProcessing Site #{site['id']}: {site['name']}")
        p_main = os.path.join(OUT_DIR, site['main_img'])
        p_inner = os.path.join(OUT_DIR, site['inner_img'])

        ok1 = capture_url(site['main_url'], p_main)
        time.sleep(1)
        ok2 = capture_url(site['inner_url'], p_inner)
        time.sleep(1)
        results[site['name']] = (ok1, ok2)

    # Also capture mobile view for 3 sites (Requirement 8)
    print("\nCapturing mobile test views for 3 sites...")
    capture_url("https://agzamov.com/", os.path.join(OUT_DIR, "mobile_agzamov.png"), is_mobile=True)
    capture_url("https://tortnadom.com/", os.path.join(OUT_DIR, "mobile_tortnadom.png"), is_mobile=True)
    capture_url("https://www.lolascupcakes.co.uk/", os.path.join(OUT_DIR, "mobile_lolas.png"), is_mobile=True)

    print("\nCapture finished! Summary:")
    for k, v in results.items():
        print(f"  {k}: main={v[0]}, inner={v[1]}")

if __name__ == "__main__":
    main()
