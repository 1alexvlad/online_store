from django.urls import path

from carts import views


app_name = 'carts'

urlpatterns = [
    path('cart_add/<slug:product_slug>/', views.CartAddView.as_view(), name='cart_add'),
    path('cart_change/<slug:product_slug>/', views.CartChangeView.as_view(), name='cart_change'),
    path('cart_remove/<int:cart_id>/', views.CartRemoveView.as_view(), name='cart_remove'),
]