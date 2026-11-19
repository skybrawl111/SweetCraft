/**
 * Асинхронный калькулятор конструктора торта (п. 8 требований)
 * Отправляет AJAX fetch к API кондитерской без перезагрузки страницы:
 * 1. Пересчитывает итоговую цену по весу, начинке, коржу и декору (Особое требование);
 * 2. Проверяет суточный лимит веса цеха на выбранную дату выдачи.
 */

document.addEventListener('DOMContentLoaded', function () {
    const weightInput = document.getElementById('id_weight');
    const fillingSelect = document.getElementById('id_filling');
    const crustSelect = document.getElementById('id_crust_type');
    const dateInput = document.getElementById('id_delivery_date');
    const decorCheckboxes = document.querySelectorAll('.decor-checkbox');
    
    const priceDisplay = document.getElementById('live-price-val');
    const dateStatusBox = document.getElementById('date-status-box');
    const submitBtn = document.getElementById('submit-order-btn');

    if (!priceDisplay || !dateStatusBox) return;

    function updateCalculation() {
        const weight = weightInput ? weightInput.value : '2.0';
        const fillingId = fillingSelect ? fillingSelect.value : '';
        const crustId = crustSelect ? crustSelect.value : '';
        const dateVal = dateInput ? dateInput.value : '';

        // Сбор ID выбранных элементов декора
        const decorIds = [];
        decorCheckboxes.forEach(cb => {
            if (cb.checked) decorIds.push(cb.value);
        });

        // Построение строки параметров
        const params = new URLSearchParams();
        params.append('weight', weight);
        if (fillingId) params.append('filling_id', fillingId);
        if (crustId) params.append('crust_id', crustId);
        if (dateVal) params.append('delivery_date', dateVal);
        decorIds.forEach(id => params.append('decor_ids[]', id));

        // Вызов fetch к бэкенду Django (п. 8)
        fetch('/api/check-date-and-price/?' + params.toString())
            .then(response => {
                if (!response.ok) {
                    throw new Error('Сетевая ошибка при расчете стоимости');
                }
                return response.json();
            })
            .then(data => {
                // 1. Обновление цены
                priceDisplay.textContent = data.price_formatted;

                // 2. Обновление статуса суточного лимита цеха
                if (!dateVal) {
                    dateStatusBox.className = 'date-status-card alert-info';
                    dateStatusBox.innerHTML = '<strong>📅 Выберите дату выдачи:</strong> чтобы система проверила свободную мощность кондитерского цеха.';
                    if (submitBtn) submitBtn.disabled = false;
                } else if (data.is_available) {
                    dateStatusBox.className = 'date-status-card alert-success';
                    dateStatusBox.innerHTML = `<strong>✅ Дата доступна:</strong> ${data.message}`;
                    if (submitBtn) submitBtn.disabled = false;
                } else {
                    dateStatusBox.className = 'date-status-card alert-danger';
                    dateStatusBox.innerHTML = `<strong>⛔ Лимит цеха превышен:</strong> ${data.message}`;
                    if (submitBtn) submitBtn.disabled = true;
                }
            })
            .catch(error => {
                console.error('Ошибка калькулятора:', error);
            });
    }

    // Слушатели событий на элементах формы
    if (weightInput) weightInput.addEventListener('input', updateCalculation);
    if (fillingSelect) fillingSelect.addEventListener('change', updateCalculation);
    if (crustSelect) crustSelect.addEventListener('change', updateCalculation);
    if (dateInput) dateInput.addEventListener('change', updateCalculation);
    decorCheckboxes.forEach(cb => cb.addEventListener('change', updateCalculation));

    // Первоначальный расчёт при загрузке страницы
    updateCalculation();
});
