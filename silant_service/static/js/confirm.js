// ========================================
// Подтверждение удаления
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    // Все ссылки и кнопки удаления
    const deleteLinks = document.querySelectorAll('.action-delete, .btn-delete, [onclick*="confirm"]');
    
    deleteLinks.forEach(link => {
        // Сохраняем оригинальный onclick
        const originalOnclick = link.getAttribute('onclick');
        
        if (originalOnclick && originalOnclick.includes('return confirm')) {
            // Уже есть confirm, оставляем как есть
            return;
        }
        
        // Добавляем подтверждение для ссылок удаления
        if (link.classList.contains('action-delete') || link.classList.contains('btn-delete')) {
            link.addEventListener('click', function(e) {
                if (!confirm('Вы уверены, что хотите удалить эту запись?')) {
                    e.preventDefault();
                    return false;
                }
            });
        }
    });
});