from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views
from .views import service_detail

urlpatterns = [
    path('', views.home, name='home'),
    path('customers/', views.customer_list, name='customer_list'),
    path('services/', views.service_list, name='service_list'),
    path('create_order/', views.create_order, name='create_order'),
    path('checkout/<int:order_id>/', views.mock_checkout, name='mock_checkout'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('customers/create/', views.create_customer, name='create_customer'),
    path('services/<int:service_id>/', service_detail, name='service_detail'),  # Define the detail view
]
