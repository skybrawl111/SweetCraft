# -*- coding: utf-8 -*-
"""
Генерация файла Excel: docs/day4/Матрица_трассировки_требований_Занятие_4.xlsx
Связывает функциональные требования (FR) с процессами Занятия 2,
функциями Занятия 3, программными модулями, тест-кейсами (Зан. 13)
и статусами проверки (Зан. 14).

Оформление: классическое черно-белое академическое (БЕЗ цветных заливок и цветного текста).
"""

import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def build_traceability_matrix():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Трассировка требований"

    # Заголовок (черный полужирный шрифт, без цветной заливки)
    ws.merge_cells("A1:H1")
    ws["A1"] = "Матрица трассировки требований информационной системы «SweetCraft» (Занятие 4, Вариант 1)"
    ws["A1"].font = Font(name="Times New Roman", size=13, bold=True, color="000000")
    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 28

    headers = [
        "Код FR",
        "Формулировка функционального требования",
        "Роль в системе",
        "Приоритет (MoSCoW)",
        "Источник требования\n(Занятия 2 и 3)",
        "Модуль / URL веб-сервиса",
        "Код тест-кейса\n(Занятие 13)",
        "Статус проверки\n(Занятие 14)"
    ]

    ws.append([]) # строка 2 пустая
    ws.append(headers) # строка 3 - шапка
    ws.row_dimensions[3].height = 32

    requirements = [
        ("FR-01", "Система должна отображать постраничный каталог готовых десертов (по 20 позиций на страницу) с фотографией, описанием, составом и базовой стоимостью.",
         "Гость, Клиент", "Must have", "Занятие 2: Процесс 1; Занятие 3: Ф-01",
         "/catalog/ | views.CatalogView | templates/catalog.html", "TC-01", "Запланирован к проверке (Занятие 14)"),

        ("FR-02", "Система должна обеспечивать текстовый поиск по названию десерта с нечувствительностью к регистру (поиск через Q-объекты icontains).",
         "Гость, Клиент", "Must have", "Занятие 2: Процесс 1; Занятие 3: Ф-02",
         "/catalog/?q= | views.CatalogView", "TC-02", "Запланирован к проверке (Занятие 14)"),

        ("FR-03", "Система должна обеспечивать фильтрацию каталога десертов по категории, типу коржа, начинке и диапазону стоимости.",
         "Гость, Клиент", "Must have", "Занятие 2: Процесс 1; Занятие 3: Ф-03",
         "/catalog/?category=&crust=&filling= | forms.CatalogFilterForm", "TC-03", "Запланирован к проверке (Занятие 14)"),

        ("FR-04", "Система должна обеспечивать сортировку каталога по трем критериям: по возрастанию цены, по убыванию цены и по популярности.",
         "Гость, Клиент", "Should have", "Занятие 2: Процесс 1; Занятие 3: Ф-01",
         "/catalog/?sort= | views.CatalogView.get_queryset()", "TC-04", "Запланирован к проверке (Занятие 14)"),

        ("FR-05", "Система должна предоставлять онлайн-конструктор для выбора веса торта от 1.5 до 12.0 кг и блокировать недопустимую ярусность (1 ярус от 1.5 кг, 2 яруса от 3 кг, 3 яруса от 5 кг).",
         "Покупатель", "Must have", "Занятие 2: Процесс 1; Занятие 3: Ф-04, Ф-05",
         "/custom-order/ | views.CustomOrderView | static/js/builder.js", "TC-05", "Запланирован к проверке (Занятие 14)"),

        ("FR-06", "Система должна обеспечивать выбор типа бисквита (классический, шоколадный, красный бархат) и авторской начинки из базы данных.",
         "Покупатель", "Must have", "Занятие 2: Процесс 1; Занятие 3: Ф-04",
         "/custom-order/ | models.CrustType, models.Filling", "TC-06", "Запланирован к проверке (Занятие 14)"),

        ("FR-07", "Система должна обеспечивать множественный выбор элементов декора (ягоды, фигурки, надписи, велюр) со связью Many-to-Many.",
         "Покупатель", "Must have", "Занятие 2: Процесс 1; Занятие 3: Ф-06",
         "/custom-order/ | models.Decoration (M:M)", "TC-07", "Запланирован к проверке (Занятие 14)"),

        ("FR-08", "Система должна производить динамический пересчет стоимости торта без перезагрузки по формуле P = (W * P_нач) + P_корж + SUM(P_декор).",
         "Клиент, Система", "Must have", "Особое требование Варианта 1; Занятие 3: Ф-08",
         "/api/calculate-price/ | views.api_calculate_price (JSON)", "TC-08", "Запланирован к проверке (Занятие 14)"),

        ("FR-09", "Система должна контролировать загрузку цеха по сменам (ConfectionerShift) и блокировать дату при исчерпании лимита (35 кг будни / 45 кг выходные).",
         "Клиент, Система", "Must have", "Особое требование Варианта 1; Занятие 2: Процессы 1, 3",
         "/api/check-date/ | views.api_check_date | models.ConfectionerShift", "TC-09", "Запланирован к проверке (Занятие 14)"),

        ("FR-10", "Система должна позволять клиенту загружать графический файл референса желаемого оформления (JPG, PNG, WebP) размером строго до 5 МБ.",
         "Покупатель", "Must have", "Занятие 2: Процесс 1; Занятие 3: Ф-07",
         "/custom-order/ | forms.OrderForm.clean_photo_sketch()", "TC-10", "Запланирован к проверке (Занятие 14)"),

        ("FR-11", "Система должна атомарно сохранять заказ и связанные позиции в БД с резервированием веса смены в единой транзакции (transaction.atomic).",
         "Система", "Must have", "Занятие 2: Процесс 1; Занятие 3: Ф-07",
         "/order/create/ | views.order_create (atomic + select_for_update)", "TC-11", "Запланирован к проверке (Занятие 14)"),

        ("FR-12", "Система должна автоматически формировать и отправлять email-уведомление клиенту с деталями заказа, стоимостью и номером накладной.",
         "Система, Клиент", "Should have", "Занятие 2: Процесс 1; Занятие 3: Ф-08",
         "bakery.services.email_service | django.core.mail.send_mail", "TC-12", "Запланирован к проверке (Занятие 14)"),

        ("FR-13", "Система должна предоставлять клиенту личный кабинет для просмотра истории заказов, текущего статуса изготовления и прикрепленных фото.",
         "Покупатель", "Should have", "Занятие 2: Процесс 3; Занятие 3: Ф-11",
         "/accounts/orders/ | views.OrderHistoryView | templates/account.html", "TC-13", "Запланирован к проверке (Занятие 14)"),

        ("FR-14", "Система должна отображать для кондитера интерактивную канбан-доску заказов в цехе со статусами («Принят», «В работе», «Готов», «Выдан»).",
         "Кондитер, Мастер", "Must have", "Занятие 2: Процесс 2; Занятие 3: Ф-10",
         "/workshop/kanban/ | views.WorkshopKanbanView", "TC-14", "Запланирован к проверке (Занятие 14)"),

        ("FR-15", "Система должна автоматически генерировать и выводить на печать технологическую карту заказа с точным расчетом сырья в граммах под вес изделия.",
         "Кондитер, Шеф", "Must have", "Занятие 2: Процесс 2; Занятие 3: Ф-12",
         "/workshop/order/<id>/tech-card/ | views.OrderTechCardView", "TC-15", "Запланирован к проверке (Занятие 14)"),

        ("FR-16", "Система должна предоставлять шеф-кондитеру и менеджеру интерфейс оперативного управления сменами, назначения мастеров и задания лимитов веса.",
         "Шеф-кондитер, Менеджер", "Must have", "Особое требование Варианта 1; Занятие 2: Процесс 2",
         "/manager/shifts/ | views.ShiftManageView | models.ConfectionerShift", "TC-16", "Запланирован к проверке (Занятие 14)"),

        ("FR-17", "Система должна позволять менеджеру управлять каталогом начинок, коржей, декоративных элементов, их базовыми ценами и остатками сырья.",
         "Менеджер", "Must have", "Занятие 3: Ф-15",
         "/manager/catalog/ | views.CatalogManageView", "TC-17", "Запланирован к проверке (Занятие 14)"),

        ("FR-18", "Система должна поддерживать ролевую модель доступа (Клиент, Кондитер, Менеджер, Администратор) с защитой производственных URL-адресов.",
         "Администратор", "Must have", "Занятие 2: Матрица RACI; Занятие 3: Ф-11",
         "bakery.models.CustomUser | django.contrib.auth | login_required", "TC-18", "Запланирован к проверке (Занятие 14)")
    ]

    # Строгие классические тонкие черные границы по ГОСТ
    thin_border = Border(
        left=Side(style='thin', color='000000'),
        right=Side(style='thin', color='000000'),
        top=Side(style='thin', color='000000'),
        bottom=Side(style='thin', color='000000')
    )

    # Оформление шапки таблицы: черный жирный текст, без цветного фона
    for col_idx, header in enumerate(headers, 1):
        cell = ws.cell(row=3, column=col_idx)
        cell.font = Font(name="Times New Roman", size=10, bold=True, color="000000")
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = thin_border

    # Заполнение строк: строго черный текст, без цветных заливок
    for row_idx, req in enumerate(requirements, start=4):
        ws.row_dimensions[row_idx].height = 26
        for col_idx, val in enumerate(req, start=1):
            cell = ws.cell(row=row_idx, column=col_idx, value=val)
            cell.font = Font(name="Times New Roman", size=9.5, color="000000")
            cell.border = thin_border

            if col_idx in [1, 7]:
                cell.alignment = Alignment(horizontal="center", vertical="center")
                cell.font = Font(name="Times New Roman", size=9.5, bold=True, color="000000")
            elif col_idx in [3, 8]:
                cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            elif col_idx == 4:
                cell.alignment = Alignment(horizontal="center", vertical="center")
                cell.font = Font(name="Times New Roman", size=9.5, bold=True, color="000000")
            else:
                cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)

    col_widths = {
        "A": 11,
        "B": 48,
        "C": 18,
        "D": 16,
        "E": 28,
        "F": 34,
        "G": 14,
        "H": 26
    }
    for col_letter, width in col_widths.items():
        ws.column_dimensions[col_letter].width = width

    ws.freeze_panes = "A4"

    filename = "docs/day4/Матрица_трассировки_требований_Занятие_4.xlsx"
    wb.save(filename)
    print(f"Матрица трассировки требований успешно сохранена в файл: {filename}")

if __name__ == "__main__":
    build_traceability_matrix()
