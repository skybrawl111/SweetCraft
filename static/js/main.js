/**
 * Основной скрипт интерфейса «SweetCraft» (Занятия 7–9)
 * 1. Мобильное бургер-меню (адаптив 360-768px);
 * 2. Клиентская валидация форм перед отправкой (маска телефона, проверка email, обязательные поля);
 * 3. Живой поиск и фильтрация каталога.
 */

document.addEventListener('DOMContentLoaded', function () {
    // -------------------------------------------------------------
    // 1. Мобильное меню-бургер (Занятия 7-8)
    // -------------------------------------------------------------
    const navToggle = document.getElementById('nav-toggle');
    const navMenu = document.getElementById('nav-menu');

    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function () {
            const isExpanded = navToggle.getAttribute('aria-expanded') === 'true';
            navToggle.setAttribute('aria-expanded', !isExpanded);
            navToggle.classList.toggle('active');
            navMenu.classList.toggle('active');
        });

        // Закрытие меню при клике вне его области
        document.addEventListener('click', function (event) {
            if (!navToggle.contains(event.target) && !navMenu.contains(event.target)) {
                navToggle.classList.remove('active');
                navMenu.classList.remove('active');
                navToggle.setAttribute('aria-expanded', 'false');
            }
        });
    }

    // -------------------------------------------------------------
    // 2. Клиентская валидация форм и маска телефона (Занятие 9)
    // -------------------------------------------------------------
    const phoneInputs = document.querySelectorAll('input[type="tel"], input[name*="phone"]');
    phoneInputs.forEach(input => {
        // Форматирование ввода номера телефона +7 (XXX) XXX-XX-XX
        input.addEventListener('input', function (e) {
            let val = input.value.replace(/\D/g, '');
            if (val.startsWith('7') || val.startsWith('8')) {
                val = val.substring(1);
            }
            let formatted = '+7 ';
            if (val.length > 0) formatted += '(' + val.substring(0, 3);
            if (val.length >= 3) formatted += ') ' + val.substring(3, 6);
            if (val.length >= 6) formatted += '-' + val.substring(6, 8);
            if (val.length >= 8) formatted += '-' + val.substring(8, 10);
            
            if (val.length === 0) {
                input.value = '';
            } else {
                input.value = formatted;
            }
        });
    });

    // Валидация перед отправкой для всех форм
    const forms = document.querySelectorAll('form[data-validate="true"], .validated-form');
    forms.forEach(form => {
        form.addEventListener('submit', function (e) {
            let isValid = true;
            const requiredFields = form.querySelectorAll('[required]');

            requiredFields.forEach(field => {
                const val = field.value.trim();
                const errorBox = field.parentElement.querySelector('.client-error-msg');
                
                if (!val) {
                    isValid = false;
                    field.classList.add('input-invalid');
                    if (errorBox) {
                        errorBox.textContent = 'Пожалуйста, заполните это обязательное поле.';
                        errorBox.style.display = 'block';
                    }
                } else if (field.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val)) {
                    isValid = false;
                    field.classList.add('input-invalid');
                    if (errorBox) {
                        errorBox.textContent = 'Введите корректный адрес электронной почты (например, name@mail.ru).';
                        errorBox.style.display = 'block';
                    }
                } else {
                    field.classList.remove('input-invalid');
                    if (errorBox) {
                        errorBox.textContent = '';
                        errorBox.style.display = 'none';
                    }
                }
            });

            if (!isValid) {
                e.preventDefault();
                const firstInvalid = form.querySelector('.input-invalid');
                if (firstInvalid) {
                    firstInvalid.focus();
                }
            }
        });
    });

    // -------------------------------------------------------------
    // 3. Динамический живой фильтр каталога (Занятие 9, Элемент 2)
    // -------------------------------------------------------------
    const liveSearchInput = document.getElementById('catalog-live-search');
    const cakeCards = document.querySelectorAll('.catalog-cake-card');

    if (liveSearchInput && cakeCards.length > 0) {
        liveSearchInput.addEventListener('input', function () {
            const query = liveSearchInput.value.toLowerCase().trim();
            cakeCards.forEach(card => {
                const title = card.getAttribute('data-title') || '';
                const desc = card.getAttribute('data-desc') || '';
                if (title.includes(query) || desc.includes(query)) {
                    card.style.display = '';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }
});
