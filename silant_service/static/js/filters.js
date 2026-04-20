// ========================================
// Дополнительная логика фильтров
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    // Кнопка "Сбросить" очищает все поля фильтров
    const resetButtons = document.querySelectorAll('.btn-reset');
    
    resetButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            // Находим ближайшую форму
            const form = this.closest('form');
            if (form) {
                // Очищаем все select и input в форме
                form.querySelectorAll('select, input[type="text"]').forEach(field => {
                    if (field.tagName === 'SELECT') {
                        field.selectedIndex = 0;
                    } else if (field.type === 'text') {
                        field.value = '';
                    }
                });
            }
        });
    });
});