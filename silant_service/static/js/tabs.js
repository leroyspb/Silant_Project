// ========================================
// Управление вкладками
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    // Находим все кнопки вкладок
    const tabBtns = document.querySelectorAll('.tab-btn');
    
    if (tabBtns.length === 0) return;
    
    // Функция переключения вкладки
    function switchTab(tabName) {
        // Скрываем все вкладки
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        
        // Убираем активный класс со всех кнопок
        tabBtns.forEach(btn => {
            btn.classList.remove('active');
        });
        
        // Показываем выбранную вкладку
        const activeTab = document.getElementById(`tab-${tabName}`);
        if (activeTab) {
            activeTab.classList.add('active');
        }
        
        // Активируем соответствующую кнопку
        const activeBtn = document.querySelector(`.tab-btn[data-tab="${tabName}"]`);
        if (activeBtn) {
            activeBtn.classList.add('active');
        }
        
        // Обновляем URL с параметром tab
        const url = new URL(window.location.href);
        url.searchParams.set('tab', tabName);
        window.history.pushState({}, '', url);
    }
    
    // Добавляем обработчики на кнопки
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabName = btn.getAttribute('data-tab');
            if (tabName) {
                switchTab(tabName);
            }
        });
    });
    
    // При загрузке страницы открываем нужную вкладку из URL
    const urlParams = new URLSearchParams(window.location.search);
    const tabParam = urlParams.get('tab');
    if (tabParam) {
        switchTab(tabParam);
    }
});