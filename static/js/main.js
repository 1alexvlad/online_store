
document.addEventListener('DOMContentLoaded', function() {
    // Улучшенная функция для AJAX-запросов
    async function sendCartRequest(url, data = {}) {
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': '{{ csrf_token }}',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: new URLSearchParams(data).toString()
            });
            
            if (!response.ok) throw new Error('Network error');
            return await response.json();
        } catch (error) {
            console.error('Cart error:', error);
            return {success: false, message: 'Ошибка при обновлении корзины'};
        }
    }

    // Функция обновления интерфейса с проверками
    function updateCartUI(data, cartItem) {
        // Обновление количества товара
        const quantityElement = cartItem.querySelector('.quantity');
        if (quantityElement && data.item_quantity !== undefined) {
            quantityElement.textContent = data.item_quantity;
        }
        
        // Обновление суммы товара
        const itemTotalElement = cartItem.querySelector('.item-total');
        if (itemTotalElement && data.item_price !== undefined) {
            itemTotalElement.textContent = data.item_price.toLocaleString() + ' ₽';
        }
        
        // Обновление общего количества
        const totalQuantityElement = document.getElementById('total-quantity');
        if (totalQuantityElement && data.total_quantity !== undefined) {
            totalQuantityElement.textContent = data.total_quantity;
        }
        
        // Обновление общей суммы
        const totalPriceElement = document.getElementById('total-price');
        if (totalPriceElement && data.total_price !== undefined) {
            totalPriceElement.textContent = data.total_price.toLocaleString() + ' ₽';
        }
    }

    // Обработчик для кнопки "+"
    document.querySelectorAll('.increase-quantity').forEach(button => {
        button.addEventListener('click', async function() {
            const url = this.dataset.url;
            const cartItem = this.closest('.cart-item');
            
            try {
                const data = await sendCartRequest(url);
                if (data.success) {
                    updateCartUI(data, cartItem);
                } else {
                    alert(data.message);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Произошла ошибка при добавлении товара');
            }
        });
    });

    // Обработчик для кнопки "-"
    document.querySelectorAll('.decrease-quantity').forEach(button => {
        button.addEventListener('click', async function() {
            const url = this.dataset.url;
            const cartItem = this.closest('.cart-item');
            
            try {
                const data = await sendCartRequest(url, {action: 'decrease'});
                if (data.success) {
                    updateCartUI(data, cartItem);
                    // Если количество 0, удаляем элемент
                    if (data.item_quantity <= 0) {
                        cartItem.remove();
                    }
                } else {
                    alert(data.message);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Произошла ошибка при уменьшении количества');
            }
        });
    });

    // Обработчик для кнопки удаления
    document.querySelectorAll('.remove-from-cart').forEach(button => {
        button.addEventListener('click', async function() {
            if (!confirm('Удалить товар из корзины?')) return;
            
            const url = this.dataset.url;
            const cartItem = this.closest('.cart-item');
            
            try {
                const data = await sendCartRequest(url);
                if (data.success) {
                    cartItem.remove();
                    updateCartUI(data, cartItem);
                } else {
                    alert(data.message);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Произошла ошибка при удалении товара');
            }
        });
    });
});  