from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_choice, name='login_choice'),   # Homepage
    path('login/', views.combined_login, name='combined_login'),  # User login
    path('register/', views.register, name='register'),  # User register
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('add/', views.add_medicine, name='add'),
    path('view/', views.view_medicines, name='view'),
    path('update/<int:id>/', views.update_medicine, name='update'),
    path('delete/<int:id>/', views.delete_medicine, name='delete'),
    path('logout/', views.logout_user, name='logout'),
    path('admin-page/', views.admin_only_view, name='admin_page'),
    path('add-to-cart/<int:medicine_id>/', views.add_to_cart, name='add_to_cart'),
    path('view-cart/', views.view_cart, name='view_cart'),
    path('buy-medicines/', views.buy_medicines, name='buy_medicines'),
    path('order-success/', views.order_success, name='order_success'),
]
