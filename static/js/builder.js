/**
 * Асинхронный калькулятор конструктора торта (Занятие 9)
 * 1. Отправляет асинхронный AJAX fetch к собственному JSON API: /api/check-date-and-price/
 * 2. Отображает индикатор загрузки (spinner) в процессе ожидания ответа;
 * 3. Пересчитывает цену в реальном времени (на десктопе и в мобильном Sticky Bottom Bar);
 * 4. Проверяет суточный лимит цеха (35 кг) и блокирует оформление при овербукинге.
 */

document.addEventListener('DOMContentLoaded', function () {
    const weightInput = document.getElementById('id_weight');
    const weightBadge = document.getElementById('weight-badge-val');
    const fillingSelect = document.getElementById('id_filling');
    const crustSelect = document.getElementById('id_crust_type');
    const dateInput = document.getElementById('id_delivery_date');
    const decorCheckboxes = document.querySelectorAll('.decor-checkbox');
    
    const priceDisplay = document.getElementById('live-price-val');
    const mobilePriceDisplay = document.getElementById('mobile-live-price');
    const dateStatusBox = document.getElementById('date-status-box');
    const submitBtn = document.getElementById('submit-order-btn');
    const spinner = document.getElementById('calc-spinner');

    if (!priceDisplay || !dateStatusBox) return;

    let abortController = null;

    function updateCalculation() {
        const weight = weightInput ? weightInput.value : '2.0';
        if (weightBadge) {
            weightBadge.textContent = `${parseFloat(weight || 0).toFixed(1)} кг`;
        }

        const fillingId = fillingSelect ? fillingSelect.value : '';
        const crustId = crustSelect ? crustSelect.value : '';
        const dateVal = dateInput ? dateInput.value : '';

        // Сбор ID выбранного декора
        const decorIds = [];
        decorCheckboxes.forEach(cb => {
            if (cb.checked) decorIds.push(cb.value);
        });

        const params = new URLSearchParams();
        params.append('weight', weight);
        if (fillingId) params.append('filling_id', fillingId);
        if (crustId) params.append('crust_id', crustId);
        if (dateVal) params.append('delivery_date', dateVal);
        decorIds.forEach(id => params.append('decor_ids[]', id));

        // Отмена предыдущего незавершенного запроса
        if (abortController) {
            abortController.abort();
        }
        abortController = new AbortController();

        // Показ индикатора загрузки (п. 4 Занятия 9)
        if (spinner) spinner.style.display = 'inline-block';

        fetch('/api/check-date-and-price/?' + params.toString(), {
            signal: abortController.signal
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Сетевая ошибка при расчете стоимости');
            }
            return response.json();
        })
        .then(data => {
            // Скрытие индикатора загрузки
            if (spinner) spinner.style.display = 'none';

            // 1. Обновление цены на десктопе и на мобильном экране
            const formattedPrice = data.price_formatted || '0 ₽';
            priceDisplay.textContent = formattedPrice;
            if (mobilePriceDisplay) {
                mobilePriceDisplay.textContent = formattedPrice;
            }

            // 2. Обновление статуса суточного лимита мощности цеха (35 кг)
            if (!dateVal) {
                dateStatusBox.className = 'alert alert-info';
                dateStatusBox.innerHTML = '<strong>📅 Укажите дату выдачи:</strong> система проверит свободную мощность цеха на этот день.';
                if (submitBtn) submitBtn.disabled = false;
            } else if (data.is_available) {
                dateStatusBox.className = 'alert alert-success';
                dateStatusBox.innerHTML = `<strong>✅ Дата свободна:</strong> ${data.message}`;
                if (submitBtn) submitBtn.disabled = false;
            } else {
                dateStatusBox.className = 'alert alert-danger';
                dateStatusBox.innerHTML = `<strong>⛔ Лимит смены исчерпан:</strong> ${data.message}`;
                if (submitBtn) submitBtn.disabled = true;
            }
        })
        .catch(err => {
            if (err.name === 'AbortError') return;
            if (spinner) spinner.style.display = 'none';
            console.error('Ошибка калькулятора:', err);
        });
    }

    // Слушатели событий
    if (weightInput) weightInput.addEventListener('input', updateCalculation);
    if (fillingSelect) fillingSelect.addEventListener('change', updateCalculation);
    if (crustSelect) crustSelect.addEventListener('change', updateCalculation);
    if (dateInput) dateInput.addEventListener('change', updateCalculation);
    decorCheckboxes.forEach(cb => cb.addEventListener('change', updateCalculation));

    // Инициализирующий пересчет
    updateCalculation();
});
