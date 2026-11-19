# -*- coding: utf-8 -*-
"""
Утилита для создания эталонных полноэкранных скриншотов веб-страниц «SweetCraft»
в двух обязательных разрешениях: Desktop 1440px и Mobile 375px.

Использует Chrome DevTools Protocol (CDP) с настоящей эмуляцией мобильных устройств
(Emulation.setDeviceMetricsOverride, User-Agent iPhone/WebKit, mobile: True).
Исключает любые элементы ОС Windows, панель задач, рамки окон и интерфейс IDE.
"""

import os
import sys
import time
import json
import base64
import socket
import struct
import urllib.request
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

class CDPClient:
    """Легковесный клиент Chrome DevTools Protocol без внешних зависимостей."""
    def __init__(self, ws_url):
        host_port_path = ws_url.replace("ws://", "").split("/", 1)
        host, port = host_port_path[0].split(":")
        path = "/" + host_port_path[1]
        self.sock = socket.create_connection((host, int(port)), timeout=20)
        handshake = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {host}:{port}\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            "Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\n"
            "Sec-WebSocket-Version: 13\r\n\r\n"
        )
        self.sock.sendall(handshake.encode('utf-8'))
        resp = self.sock.recv(4096)
        if b"101" not in resp:
            raise RuntimeError(f"CDP WebSocket handshake failed: {resp[:200]}")
        self.msg_id = 1

    def send_cmd(self, method, params=None):
        mid = self.msg_id
        self.msg_id += 1
        payload = json.dumps({"id": mid, "method": method, "params": params or {}}).encode('utf-8')
        mask = os.urandom(4)
        length = len(payload)
        if length <= 125:
            header = bytes([0x81, 0x80 | length])
        elif length <= 65535:
            header = struct.pack('!BBH', 0x81, 0x80 | 126, length)
        else:
            header = struct.pack('!BBQ', 0x81, 0x80 | 127, length)
        masked = bytearray(length)
        for i in range(length):
            masked[i] = payload[i] ^ mask[i % 4]
        self.sock.sendall(header + mask + bytes(masked))

        while True:
            h = self.sock.recv(2)
            if not h or len(h) < 2:
                continue
            b1, b2 = h[0], h[1]
            l = b2 & 0x7F
            if l == 126:
                l = struct.unpack('!H', self.sock.recv(2))[0]
            elif l == 127:
                l = struct.unpack('!Q', self.sock.recv(8))[0]
            buf = bytearray()
            while len(buf) < l:
                chunk = self.sock.recv(min(l - len(buf), 65536))
                if not chunk:
                    break
                buf.extend(chunk)
            try:
                data = json.loads(buf.decode('utf-8', errors='ignore'))
            except:
                continue
            if data.get("id") == mid:
                return data.get("result", {})

    def close(self):
        try:
            self.sock.close()
        except:
            pass


def capture_all():
    print("=== Запуск локального тестового WSGI-сервера на 127.0.0.1:8000 ===")
    httpd = make_server('127.0.0.1', 8000, application)
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    time.sleep(1)

    print(f"Запуск Chrome Headless с CDP-портом 9222: {CHROME_PATH}")
    chrome_proc = subprocess.Popen([
        CHROME_PATH,
        '--headless=new',
        '--disable-gpu',
        '--no-sandbox',
        '--remote-debugging-port=9222',
        'about:blank'
    ])
    time.sleep(2)

    try:
        tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json').read())
        page_tab = [x for x in tabs if x.get('type') == 'page'][0]
        cdp = CDPClient(page_tab['webSocketDebuggerUrl'])
        cdp.send_cmd('Page.enable')

        for page_name, url_path in PAGES:
            target_url = f"http://127.0.0.1:8000{url_path}"

            # 1. Desktop 1440x950
            cdp.send_cmd('Network.setUserAgentOverride', {
                'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            })
            cdp.send_cmd('Emulation.setDeviceMetricsOverride', {
                'width': 1440,
                'height': 950,
                'deviceScaleFactor': 1,
                'mobile': False
            })
            cdp.send_cmd('Page.navigate', {'url': target_url})
            time.sleep(1.2)
            d_res = cdp.send_cmd('Page.captureScreenshot', {
                'format': 'png',
                'clip': {'x': 0, 'y': 0, 'width': 1440, 'height': 950, 'scale': 1}
            })
            if 'data' in d_res:
                out_desktop = OUTPUT_DIR / f"desktop_1440_{page_name}.png"
                with open(out_desktop, 'wb') as f:
                    f.write(base64.b64decode(d_res['data']))
                print(f"✓ Desktop [1440x950]: {page_name:<12} -> {out_desktop.name}")

            # 2. Mobile 375x812 (Истинная мобильная эмуляция iPhone/WebKit)
            cdp.send_cmd('Network.setUserAgentOverride', {
                'userAgent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
            })
            cdp.send_cmd('Emulation.setDeviceMetricsOverride', {
                'width': 375,
                'height': 812,
                'deviceScaleFactor': 2,
                'mobile': True,
                'screenOrientation': {'type': 'portraitPrimary', 'angle': 0}
            })
            cdp.send_cmd('Page.navigate', {'url': target_url})
            time.sleep(1.2)
            m_res = cdp.send_cmd('Page.captureScreenshot', {
                'format': 'png',
                'clip': {'x': 0, 'y': 0, 'width': 375, 'height': 812, 'scale': 2}
            })
            if 'data' in m_res:
                out_mobile = OUTPUT_DIR / f"mobile_375_{page_name}.png"
                with open(out_mobile, 'wb') as f:
                    f.write(base64.b64decode(m_res['data']))
                print(f"✓ Mobile  [375x812]:  {page_name:<12} -> {out_mobile.name}")

        cdp.close()
        print("=== Все полноэкранные десктопные и мобильные скриншоты успешно сняты! ===")
    finally:
        chrome_proc.terminate()
        httpd.shutdown()

if __name__ == "__main__":
    capture_all()
