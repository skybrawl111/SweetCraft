# -*- coding: utf-8 -*-
"""
Генерация файла Excel: docs/day3/Матрица_функций_Занятие_3.xlsx
Содержит 16 функций, 10 сайтов-аналогов, статус (Есть, Нет, Частично),
подсчет по формуле COUNTIF и привязку к приоритетам нашего проекта.
"""

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def build_excel_matrix():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Матрица функций"

    # Title
    ws.merge_cells("A1:M1")
    ws["A1"] = "Матрица функционального анализа 10 сайтов-аналогов (Занятие 3, Вариант 1)"
    ws["A1"].font = Font(name="Times New Roman", size=14, bold=True, color="1F497D")
    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 30

    headers = [
        "№", "Функция системы",
        "agzamov.com\n(РФ)", "sweetmarin.ru\n(РФ)", "teabakery.ru\n(РФ)",
        "british-bakery.ru\n(РФ)", "cake-time.ru\n(РФ)", "tortnadom.com\n(РФ)",
        "irisdelicia.ru\n(РФ)", "napoleoncake.ru\n(РФ)", "magnoliabakery.com\n(США)",
        "lolascupcakes.co.uk\n(UK)", "Итого есть\n(из 10)"
    ]

    ws.append([]) # row 2 empty
    ws.append(headers) # row 3
    ws.row_dimensions[3].height = 40

    data = [
        (1, "Каталог готовых изделий с фото и описанием", "Есть", "Есть", "Есть", "Есть", "Есть", "Есть", "Есть", "Есть", "Есть", "Есть"),
        (2, "Текстовый поиск по каталогу (icontains)", "Нет", "Есть", "Нет", "Есть", "Есть", "Есть", "Есть", "Нет", "Есть", "Есть"),
        (3, "Фильтрация каталога по 3+ параметрам", "Нет", "Есть", "Нет", "Есть", "Есть", "Есть", "Есть", "Нет", "Есть", "Есть"),
        (4, "Выбор типа основы / бисквита", "Есть", "Есть", "Частично", "Есть", "Есть", "Есть", "Есть", "Нет", "Есть", "Есть"),
        (5, "Выбор авторской начинки из перечня", "Есть", "Есть", "Есть", "Есть", "Есть", "Есть", "Есть", "Есть", "Есть", "Есть"),
        (6, "Множественный выбор элементов декора (M:M)", "Нет", "Частично", "Нет", "Нет", "Частично", "Есть", "Есть", "Нет", "Частично", "Есть"),
        (7, "Прикрепление фото-эскиза клиентом (до 5 МБ)", "Есть", "Частично", "Нет", "Нет", "Есть", "Есть", "Есть", "Нет", "Нет", "Есть"),
        (8, "Живой расчет цены в реальном времени (fetch)", "Нет", "Частично", "Нет", "Нет", "Нет", "Частично", "Есть", "Нет", "Есть", "Есть"),
        (9, "Контроль суточного веса цеха / автоблок даты", "Нет", "Нет", "Нет", "Нет", "Нет", "Нет", "Нет", "Нет", "Есть", "Есть"),
        (10, "Выбор даты и тайм-слота получения десерта", "Нет", "Есть", "Есть", "Есть", "Частично", "Есть", "Есть", "Есть", "Есть", "Есть"),
        (11, "Личный кабинет покупателя с заказами", "Нет", "Есть", "Нет", "Есть", "Нет", "Частично", "Есть", "Нет", "Есть", "Есть"),
        (12, "CRUD отзывов покупателей с оценкой 1-5 звезд", "Нет", "Есть", "Нет", "Частично", "Нет", "Есть", "Есть", "Нет", "Есть", "Есть"),
        (13, "Автогенерация печатного наряда для кондитера", "Нет", "Нет", "Нет", "Нет", "Нет", "Нет", "Нет", "Нет", "Частично", "Частично"),
        (14, "Онлайн-оплата банковской картой на сайте", "Нет", "Есть", "Есть", "Есть", "Нет", "Есть", "Есть", "Есть", "Есть", "Есть"),
        (15, "Калькулятор зон доставки по карте/зонам", "Нет", "Есть", "Есть", "Есть", "Нет", "Есть", "Есть", "Нет", "Частично", "Есть"),
        (16, "Адаптивная вёрстка под мобильные экраны", "Частично", "Есть", "Есть", "Есть", "Частично", "Частично", "Есть", "Есть", "Есть", "Есть")
    ]

    thin_border = Border(
        left=Side(style='thin', color='A6A6A6'),
        right=Side(style='thin', color='A6A6A6'),
        top=Side(style='thin', color='A6A6A6'),
        bottom=Side(style='thin', color='A6A6A6')
    )
    header_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
    fill_yes = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid") # green
    fill_part = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid") # yellow
    fill_no = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid") # gray

    for r_idx, row_data in enumerate(data, start=4):
        num, fname, *sites = row_data
        formula = f'=COUNTIF(C{r_idx}:L{r_idx}, "Есть") + COUNTIF(C{r_idx}:L{r_idx}, "Частично")*0.5'
        row_vals = [num, fname] + sites + [formula]
        ws.append(row_vals)
        ws.row_dimensions[r_idx].height = 24

    # Styling header
    for col_idx in range(1, 14):
        cell = ws.cell(row=3, column=col_idx)
        cell.font = Font(name="Times New Roman", size=11, bold=True, color="1F497D")
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = thin_border

    # Styling data
    for r in range(4, 20):
        for c in range(1, 14):
            cell = ws.cell(row=r, column=c)
            cell.font = Font(name="Times New Roman", size=10)
            cell.border = thin_border
            if c == 1:
                cell.alignment = Alignment(horizontal="center", vertical="center")
            elif c == 2:
                cell.alignment = Alignment(horizontal="left", vertical="center")
            elif 3 <= c <= 12:
                cell.alignment = Alignment(horizontal="center", vertical="center")
                val = str(cell.value)
                if val == "Есть":
                    cell.fill = fill_yes
                    cell.font = Font(name="Times New Roman", size=10, bold=True, color="276A3C")
                elif val == "Частично":
                    cell.fill = fill_part
                    cell.font = Font(name="Times New Roman", size=10, italic=True, color="8A6D3B")
                else:
                    cell.fill = fill_no
                    cell.font = Font(name="Times New Roman", size=10, color="7F7F7F")
            elif c == 13:
                cell.alignment = Alignment(horizontal="center", vertical="center")
                cell.font = Font(name="Times New Roman", size=11, bold=True, color="1F497D")
                cell.fill = header_fill

    # Adjust column widths
    ws.column_dimensions['A'].width = 5
    ws.column_dimensions['B'].width = 44
    for c in range(3, 13):
        col_letter = get_column_letter(c)
        ws.column_dimensions[col_letter].width = 15
    ws.column_dimensions['M'].width = 14

    out_xlsx = r"c:\Users\Чошгун\Desktop\Praktika1\docs/day3/Матрица_функций_Занятие_3.xlsx"
    wb.save(out_xlsx)
    print(f"Excel matrix saved successfully: {out_xlsx}")

if __name__ == "__main__":
    build_excel_matrix()
