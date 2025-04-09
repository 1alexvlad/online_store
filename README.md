# Тестовое задание на должность Python/Django-разработчик

### Запустите проект 
```python
python manage.py runserver
```


Приложение product.views:
- MainView - отображает базовую страницу
- CatalogProduct - отображает каталог товаров и фильтрацию по ним
- ProductDetail - детальная информация о конкретном товаре
- Search - поиск по товарам

Приложение order.views:
- CreateOrderView - Создает заказ

Приложение cart.views:
- CartAddView - добавляет +1 к количества продукта в корзине
- CartChangeView - умеьшает -1 к количества продукта в корзине
- CartRemoveView - удаляет товар из корзины
  
Приложение account.views:
- RegistrationView - регистрация пользователя
- UserLoginView - аунтификация пользователя
- logout_user - выход пользователя
- ProfileView - обзор истории покупок
- UsersCart - отображает корзину с количеством товара


``Данные для superuser username - vlad, password - 123``

``Данные обычного пользовтеля username - user, password - 7297129570941866 ``

