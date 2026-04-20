// ========================================
// Основные скрипты
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    
    // Автоматическое скрытие сообщений об ошибках через 5 секунд
    const errorMessages = document.querySelectorAll('.error-message, .form-errors');
    if (errorMessages.length > 0) {
        setTimeout(() => {
            errorMessages.forEach(msg => {
                msg.style.transition = 'opacity 0.5s';
                msg.style.opacity = '0';
                setTimeout(() => {
                    msg.style.display = 'none';
                }, 500);
            });
        }, 5000);
    }
    
    // Подсветка активной ссылки в навигации
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-links a');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href && currentPath.includes(href) && href !== '/') {
            link.style.backgroundColor = 'rgba(255, 255, 255, 0.2)';
            link.style.borderRadius = '4px';
        }
    });
    
    // Улучшение работы фильтров - сохранение значений при отправке
    const filterForms = document.querySelectorAll('.filters-form');
    filterForms.forEach(form => {
        // Добавляем скрытое поле с текущей вкладкой если его нет
        if (!form.querySelector('input[name="tab"]')) {
            const activeTab = document.querySelector('.tab-btn.active');
            if (activeTab) {
                const tabInput = document.createElement('input');
                tabInput.type = 'hidden';
                tabInput.name = 'tab';
                tabInput.value = activeTab.getAttribute('data-tab');
                form.appendChild(tabInput);
            }
        }
    });
});