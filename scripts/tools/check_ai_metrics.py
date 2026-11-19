# -*- coding: utf-8 -*-
import re
import math
from pathlib import Path
from collections import Counter
import docx

DOCX_PATH = Path("docs/day6/Отчет_Занятие_6_Вариант_1_Финальный.docx")

def run_audit():
    doc = docx.Document(DOCX_PATH)
    
    full_paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    table_texts = []
    for t in doc.tables:
        for r in t.rows:
            for c in r.cells:
                if c.text.strip():
                    table_texts.append(c.text.strip())
                    
    all_text = "\n".join(full_paragraphs + table_texts)
    
    # Словник
    words = re.findall(r'[а-яА-Яa-zA-Z0-9\-]+', all_text.lower())
    total_words = len(words)
    vocab = set(words)
    ttr = len(vocab) / total_words if total_words else 0
    
    # Предложения
    sents = [s.strip() for s in re.split(r'[.!?]+', "\n".join(full_paragraphs)) if len(s.strip()) > 3]
    sent_lens = [len(re.findall(r'[а-яА-Яa-zA-Z0-9\-]+', s)) for s in sents]
    
    mean_l = sum(sent_lens) / len(sent_lens) if sent_lens else 0
    var_l = sum((x - mean_l)**2 for x in sent_lens) / len(sent_lens) if sent_lens else 0
    std_l = math.sqrt(var_l)
    cv = std_l / mean_l if mean_l else 0
    
    # ИИ-маркеры
    ai_cliches = [
        "в современном мире", "в современном обществе", "нельзя не отметить",
        "следует подчеркнуть", "следует отметить", "играет важную роль",
        "играет ключевую роль", "является неотъемлемой частью", "актуальность данной темы",
        "таким образом можно сделать вывод", "подводя итоги вышесказанному", "в заключение хочется сказать",
        "важно помнить", "необходимо учитывать тот факт", "погрузимся в", "рассмотрим поподробнее",
        "давайте рассмотрим", "не секрет, что", "как известно", "в конечном счете", "в сухом остатке",
        "не стоит забывать", "имеет колоссальное значение", "гармонично сочетает", "широкий спектр",
        "воплощает в себе", "на сегодняшний день", "в сегодняшних реалиях", "стоит отметить",
        "подводя итоги", "как было сказано выше"
    ]
    
    found_cliches = [c for c in ai_cliches if c in all_text.lower()]
    
    # Частота вводных слов связок
    fillers = {
        "кроме того": len(re.findall(r'\bкроме того\b', all_text.lower())),
        "таким образом": len(re.findall(r'\bтаким образом\b', all_text.lower())),
        "в частности": len(re.findall(r'\bв частности\b', all_text.lower())),
        "позволяет": len(re.findall(r'\bпозволяет\b', all_text.lower())),
        "обеспечивает": len(re.findall(r'\bобеспечивает\b', all_text.lower())),
        "является": len(re.findall(r'\bявляется\b', all_text.lower())),
        "следует": len(re.findall(r'\bследует\b', all_text.lower())),
        "необходимо": len(re.findall(r'\bнеобходимо\b', all_text.lower())),
    }
    
    # Анализ длины предложений по корзинам
    buckets = {
        "Короткие (1-7 слов)": sum(1 for l in sent_lens if l <= 7),
        "Средние (8-16 слов)": sum(1 for l in sent_lens if 8 <= l <= 16),
        "Длинные (17-25 слов)": sum(1 for l in sent_lens if 17 <= l <= 25),
        "Очень длинные (>25 слов)": sum(1 for l in sent_lens if l > 25),
    }
    
    print("=" * 60)
    print("      ИТОГОВЫЙ АУДИТ НА ПРИЗНАКИ НЕЙРОСЕТИ (ИИ-ДЕТЕКТОР)")
    print("=" * 60)
    print(f"Общее количество слов в документе: {total_words}")
    print(f"Количество уникальных слов:         {len(vocab)}")
    print(f"Коэффициент лексического богатства (TTR): {ttr:.4f}")
    print(f"  -> Оценка: {'ОТЛИЧНО (Богатая речь)' if ttr > 0.45 else 'НОРМА' if ttr > 0.38 else 'РИСК (Бедный язык)'}")
    print(f"Средняя длина предложения:         {mean_l:.2f} слов")
    print(f"Стандартное отклонение длины:       {std_l:.2f}")
    print(f"Коэффициент вариативности (Burstiness): {cv:.4f}")
    print(f"  -> Оценка: {'ОТЛИЧНО (Высокая вариативность человека)' if cv > 0.60 else 'РИСК (Монотонный робот)'}")
    print("-" * 60)
    print("Распределение предложений по длине (человеческий ритм):")
    for b_name, b_val in buckets.items():
        pct = (b_val / len(sent_lens)) * 100 if sent_lens else 0
        bar = "█" * int(pct // 4)
        print(f"  {b_name:<26}: {b_val:>3} ({pct:>5.1f}%) {bar}")
    print("-" * 60)
    print("Поиск типичных ИИ-маркеров и клише (31 фраза):")
    if found_cliches:
        print(f"  ВНИМАНИЕ! Найдено совпадений: {len(found_cliches)}")
        for cl in found_cliches:
            print(f"    - {cl}")
    else:
        print("  ИИ-маркеры и клише не обнаружены (0 совпадений). Текст 100% чист.")
    print("-" * 60)
    print("Частота стандартных глаголов-связок:")
    for f_w, f_c in fillers.items():
        pct = (f_c / total_words) * 100
        print(f"  - '{f_w}': {f_c} вхождений ({pct:.2f}%)")
    print("=" * 60)

if __name__ == "__main__":
    run_audit()
