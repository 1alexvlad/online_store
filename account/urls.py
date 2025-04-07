from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('users-cart/', views.UsersCart.as_view(), name='users-cart'),
]
