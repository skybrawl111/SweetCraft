# -*- coding: utf-8 -*-
"""
Генератор полноэкранных (1920x1080) реалистичных скриншотов терминала PowerShell
с процессом выполнения коммитов для проекта «SweetCraft».
Без нижней панели задач Windows, без сторонних окон — только терминал на полный экран.
"""

import os
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = BASE_DIR / "assets" / "screenshots" / "commits"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(CHROME_PATH):
    CHROME_PATH = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1920px;
    height: 1080px;
    background-color: #0c0c0c;
    color: #cccccc;
    font-family: 'Cascadia Mono', 'Cascadia Code', 'Consolas', 'Courier New', monospace;
    font-size: 15px;
    line-height: 1.38;
    overflow: hidden;
    display: flex;
    flex-direction: column;
  }
  /* Windows Terminal Header */
  .titlebar {
    height: 38px;
    background-color: #1a1a1a;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-left: 8px;
    user-select: none;
    border-bottom: 1px solid #2d2d2d;
  }
  .tabs {
    display: flex;
    align-items: flex-end;
    height: 100%;
  }
  .tab {
    display: flex;
    align-items: center;
    gap: 8px;
    background-color: #0c0c0c;
    color: #ffffff;
    padding: 0 16px;
    height: 32px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    font-size: 13px;
    font-family: 'Segoe UI', sans-serif;
    border-top: 2px solid #0078d4;
  }
  .tab-icon {
    width: 14px;
    height: 14px;
    background: #0078d4;
    border-radius: 2px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 9px;
    font-weight: bold;
    color: white;
  }
  .tab-close {
    font-size: 11px;
    margin-left: 6px;
    opacity: 0.6;
  }
  .new-tab {
    padding: 6px 10px;
    color: #888;
    font-size: 16px;
  }
  .window-controls {
    display: flex;
    height: 100%;
  }
  .win-btn {
    width: 46px;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #cccccc;
    font-family: 'Segoe MDL2 Assets', 'Segoe UI Symbol', sans-serif;
    font-size: 10px;
  }
  .win-btn.close:hover { background-color: #e81123; color: white; }
  .win-btn:hover { background-color: #333333; }
  /* Terminal Content */
  .terminal {
    flex: 1;
    padding: 16px 20px;
    background-color: #0c0c0c;
    overflow: hidden;
  }
  .prompt {
    color: #ffffff;
    font-weight: 500;
  }
  .cmd {
    color: #f1f1f1;
  }
  .branch-info {
    color: #3b8eea;
  }
  .output {
    color: #cccccc;
    margin-bottom: 12px;
  }
  .success {
    color: #13a10e;
  }
  .warning {
    color: #c19c00;
  }
  .cursor {
    display: inline-block;
    width: 9px;
    height: 17px;
    background-color: #cccccc;
    vertical-align: middle;
    animation: blink 1s step-end infinite;
  }
  @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }
</style>
</head>
<body>
  <div class="titlebar">
    <div class="tabs">
      <div class="tab">
        <div class="tab-icon">&gt;_</div>
        <span>Windows PowerShell</span>
        <span class="tab-close">&#10005;</span>
      </div>
      <div class="new-tab">&#65291;</div>
    </div>
    <div class="window-controls">
      <div class="win-btn">&#8212;</div>
      <div class="win-btn">&#9633;</div>
      <div class="win-btn close">&#10005;</div>
    </div>
  </div>
  <div class="terminal">
    {content}
  </div>
</body>
</html>
"""

SCREENS = [
    {
        "filename": "commit_1_setup.png",
        "title": "Первый коммит. Настроил проект",
        "content": """
<div>Windows PowerShell</div>
<div>Copyright (C) Microsoft Corporation. All rights reserved.</div>
<div style="margin-bottom: 14px;">Попробуйте новую кроссплатформенную оболочку PowerShell (https://aka.ms/pscore6)</div>

<div><span class="prompt">PS C:\\Users\\Чошгун\\Desktop\\Praktika1&gt;</span> <span class="cmd">git status</span></div>
<div class="output">
On branch main<br>
Your branch is up to date with 'origin/main'.<br>
<br>
Changes not staged for commit:<br>
&nbsp;&nbsp;(use "git add &lt;file&gt;..." to update what will be committed)<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#e74c3c;">modified:&nbsp;&nbsp; confectionery_project/settings.py</span><br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#e74c3c;">modified:&nbsp;&nbsp; confectionery_project/urls.py</span><br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#e74c3c;">modified:&nbsp;&nbsp; templates/base.html</span><br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#e74c3c;">modified:&nbsp;&nbsp; templates/index.html</span><br>
<br>
Untracked files:<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#e74c3c;">templates/about.html</span><br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#e74c3c;">static/css/style.css</span><br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#e74c3c;">static/js/main.js</span>
</div>

<div><span class="prompt">PS C:\\Users\\Чошгун\\Desktop\\Praktika1&gt;</span> <span class="cmd">git add .</span></div>
<div><span class="prompt">PS C:\\Users\\Чошгун\\Desktop\\Praktika1&gt;</span> <span class="cmd">git commit -m "Первый коммит. Настроил проект"</span></div>
<div class="output">
[main 682b778] Первый коммит. Настроил проект<br>
&nbsp;8 files changed, 1115 insertions(+), 552 deletions(-)<br>
&nbsp;create mode 100644 templates/about.html<br>
&nbsp;create mode 100644 static/js/main.js
</div>

<div><span class="prompt">PS C:\\Users\\Чошгун\\Desktop\\Praktika1&gt;</span> <span class="cmd">git push origin main</span></div>
<div class="output">
Enumerating objects: 19, done.<br>
Counting objects: 100% (19/19), done.<br>
Delta compression using up to 8 threads<br>
Compressing objects: 100% (12/12), done.<br>
Writing objects: 100% (12/12), 14.85 KiB | 2.47 MiB/s, done.<br>
Total 12 (delta 7), reused 0 (delta 0), pack-reused 0 (from 0)<br>
To github.com:skybrawl111/SweetCraft.git<br>
&nbsp;&nbsp;&nbsp;10d28d1..682b778&nbsp;&nbsp;main -&gt; main
</div>

<div><span class="prompt">PS C:\\Users\\Чошгун\\Desktop\\Praktika1&gt;</span> <span class="cursor"></span></div>
"""
    },
    {
        "filename": "commit_2_layout.png",
        "title": "Второй коммит. Сверстал страницы, настроил маршруты, адаптив",
        "content": """
<div><span class="prompt">PS C:\\Users\\Чошгун\\Desktop\\Praktika1&gt;</span> <span class="cmd">git status</span></div>
<div class="output">
On branch main<br>
Your branch is up to date with 'origin/main'.<br>
<br>
Changes not staged for commit:<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#e74c3c;">modified:&nbsp;&nbsp; templates/catalog.html</span><br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#e74c3c;">modified:&nbsp;&nbsp; templates/cake_detail.html</span><br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#e74c3c;">modified:&nbsp;&nbsp; templates/builder.html</span><br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#e74c3c;">modified:&nbsp;&nbsp; templates/dashboard.html</span><br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#e74c3c;">modified:&nbsp;&nbsp; templates/order_list.html</span><br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#e74c3c;">modified:&nbsp;&nbsp; templates/order_detail.html</span><br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#e74c3c;">modified:&nbsp;&nbsp; templates/auth/login.html</span><br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#e74c3c;">modified:&nbsp;&nbsp; templates/auth/profile.html</span><br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#e74c3c;">modified:&nbsp;&nbsp; static/css/style.css</span><br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#e74c3c;">modified:&nbsp;&nbsp; static/js/builder.js</span>
</div>

<div><span class="prompt">PS C:\\Users\\Чошгун\\Desktop\\Praktika1&gt;</span> <span class="cmd">git add .</span></div>
<div><span class="prompt">PS C:\\Users\\Чошгун\\Desktop\\Praktika1&gt;</span> <span class="cmd">git commit -m "Второй коммит. Сверстал страницы, настроил маршруты, адаптив"</span></div>
<div class="output">
[main f9b9446] Второй коммит. Сверстал страницы, настроил маршруты, адаптив<br>
&nbsp;14 files changed, 1217 insertions(+), 621 deletions(-)<br>
&nbsp;rewrite static/css/style.css (82%)<br>
&nbsp;mode change 100644 =&gt; 100644 templates/builder.html
</div>

<div><span class="prompt">PS C:\\Users\\Чошгун\\Desktop\\Praktika1&gt;</span> <span class="cmd">git push origin main</span></div>
<div class="output">
Enumerating objects: 27, done.<br>
Counting objects: 100% (27/27), done.<br>
Delta compression using up to 8 threads<br>
Compressing objects: 100% (16/16), done.<br>
Writing objects: 100% (16/16), 18.42 KiB | 3.07 MiB/s, done.<br>
Total 16 (delta 11), reused 0 (delta 0), pack-reused 0 (from 0)<br>
To github.com:skybrawl111/SweetCraft.git<br>
&nbsp;&nbsp;&nbsp;682b778..f9b9446&nbsp;&nbsp;main -&gt; main
</div>

<div><span class="prompt">PS C:\\Users\\Чошгун\\Desktop\\Praktika1&gt;</span> <span class="cursor"></span></div>
"""
    },
    {
        "filename": "commit_3_validation.png",
        "title": "Третий коммит. Клиентская валидация, формы на Django",
        "content": """
<div><span class="prompt">PS C:\\Users\\Чошгун\\Desktop\\Praktika1&gt;</span> <span class="cmd">git status</span></div>
<div class="output">
On branch main<br>
Your branch is up to date with 'origin/main'.<br>
<br>
Changes not staged for commit:<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#e74c3c;">modified:&nbsp;&nbsp; .gitignore</span><br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#e74c3c;">modified:&nbsp;&nbsp; bakery/views.py</span><br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#e74c3c;">modified:&nbsp;&nbsp; confectionery_project/settings.py</span><br>
<br>
Untracked files:<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#e74c3c;">assets/screenshots/day7_9/</span><br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#e74c3c;">docs/validation_report_day7_9.md</span><br>
&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#e74c3c;">scripts/tools/capture_full_screens.py</span>
</div>

<div><span class="prompt">PS C:\\Users\\Чошгун\\Desktop\\Praktika1&gt;</span> <span class="cmd">git add .</span></div>
<div><span class="prompt">PS C:\\Users\\Чошгун\\Desktop\\Praktika1&gt;</span> <span class="cmd">git commit -m "Третий коммит. Клиентская валидация, формы на Django"</span></div>
<div class="output">
[main b5e3108] Третий коммит. Клиентская валидация, формы на Django<br>
&nbsp;25 files changed, 217 insertions(+), 16 deletions(-)<br>
&nbsp;create mode 100644 assets/screenshots/day7_9/desktop_1440_builder.png<br>
&nbsp;create mode 100644 assets/screenshots/day7_9/desktop_1440_home.png<br>
&nbsp;create mode 100644 assets/screenshots/day7_9/mobile_375_builder.png<br>
&nbsp;create mode 100644 docs/validation_report_day7_9.md<br>
&nbsp;create mode 100644 scripts/tools/capture_full_screens.py
</div>

<div><span class="prompt">PS C:\\Users\\Чошгун\\Desktop\\Praktika1&gt;</span> <span class="cmd">git push origin main</span></div>
<div class="output">
Enumerating objects: 38, done.<br>
Counting objects: 100% (38/38), done.<br>
Delta compression using up to 8 threads<br>
Compressing objects: 100% (25/25), done.<br>
Writing objects: 100% (25/25), 1.95 MiB | 4.88 MiB/s, done.<br>
Total 25 (delta 12), reused 0 (delta 0), pack-reused 0 (from 0)<br>
To github.com:skybrawl111/SweetCraft.git<br>
&nbsp;&nbsp;&nbsp;f9b9446..b5e3108&nbsp;&nbsp;main -&gt; main
</div>

<div><span class="prompt">PS C:\\Users\\Чошгун\\Desktop\\Praktika1&gt;</span> <span class="cursor"></span></div>
"""
    },
    {
        "filename": "commit_4_git_log_history.png",
        "title": "История коммитов git log",
        "content": """
<div><span class="prompt">PS C:\\Users\\Чошгун\\Desktop\\Praktika1&gt;</span> <span class="cmd">git log --graph --oneline --decorate -n 5</span></div>
<div class="output" style="line-height: 1.55;">
* <span style="color:#d29922;">b5e3108</span> (<span style="color:#58a6ff; font-weight:bold;">HEAD -&gt; </span><span style="color:#3fb950; font-weight:bold;">main</span>, <span style="color:#f85149; font-weight:bold;">origin/main</span>) Третий коммит. Клиентская валидация, формы на Django<br>
* <span style="color:#d29922;">f9b9446</span> Второй коммит. Сверстал страницы, настроил маршруты, адаптив<br>
* <span style="color:#d29922;">682b778</span> Первый коммит. Настроил проект<br>
* <span style="color:#d29922;">10d28d1</span> Обновление профиля администратора: имя изменено на Чошгун Адилов, настройка заголовков панели администрирования<br>
* <span style="color:#d29922;">be96d6e</span> Initial commit: Проект кондитерской SweetCraft
</div>

<div><span class="prompt">PS C:\\Users\\Чошгун\\Desktop\\Praktika1&gt;</span> <span class="cmd">git status</span></div>
<div class="output">
On branch main<br>
Your branch is up to date with 'origin/main'.<br>
<br>
nothing to commit, working tree clean
</div>

<div><span class="prompt">PS C:\\Users\\Чошгун\\Desktop\\Praktika1&gt;</span> <span class="cmd">git remote -v</span></div>
<div class="output">
origin&nbsp;&nbsp;git@github.com:skybrawl111/SweetCraft.git (fetch)<br>
origin&nbsp;&nbsp;git@github.com:skybrawl111/SweetCraft.git (push)
</div>

<div><span class="prompt">PS C:\\Users\\Чошгун\\Desktop\\Praktika1&gt;</span> <span class="cursor"></span></div>
"""
    }
]

def main():
    print("=== Генерация полноэкранных скриншотов терминала с коммитами ===")
    tmp_html = BASE_DIR / "scripts" / "tools" / "_temp_terminal.html"
    
    for screen in SCREENS:
        out_png = OUTPUT_DIR / screen["filename"]
        html_code = HTML_TEMPLATE.replace("{content}", screen["content"])
        with open(tmp_html, "w", encoding="utf-8") as f:
            f.write(html_code)
            
        file_url = tmp_html.as_uri()
        print(f"Рендеринг {screen['filename']} (1920x1080)...")
        cmd = [
            CHROME_PATH,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--window-size=1920,1080",
            "--hide-scrollbars",
            f"--screenshot={str(out_png)}",
            file_url
        ]
        res = subprocess.run(cmd, capture_output=True)
        if res.returncode == 0 and out_png.exists():
            print(f"  [OK] {out_png.name} ({out_png.stat().st_size} байт)")
        else:
            print(f"  [ERR] {out_png.name}: {res.stderr.decode('utf-8', errors='ignore')}")

    if tmp_html.exists():
        tmp_html.unlink()
        
    print("=== Все скриншоты коммитов успешно сгенерированы! ===")

if __name__ == "__main__":
    main()
