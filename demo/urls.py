from django.urls import path
from django.contrib.auth import views as auth_views

from demo import views
from demo.views import *

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('validate_username', validate_username, name='validate_username'),
    path('validate_email', validate_email, name='validate_email'),

    path('', catalog, name='catalog'),
    path('about', about, name='about'),
    path('contact', contact, name='contact'),
    path('product/<pk>', product, name='product'),
    path('delete_order/<pk>', delete_order, name='delete_order'),

    path('orders', orders, name='orders'),
    path('basket', basket, name='basket')

]
