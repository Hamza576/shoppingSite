from django.urls import path
from accounts import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # path('', views.home, name='home'),
    path('registration/', views.registration, name='registration'),
    path('activate/<str:uidb64>/<str:token>/', views.activate_account, name="activate"),
    path('login/', views.login_view, name='login'),
    path('password_reset/', views.password_reset_view, name='password_reset'),
    path('password_reset_confirm/<str:uidb64>/<str:token>/', views.password_reset_confirm_view, name='password_reset_confirm'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('order_detail/<str:order_number>', views.order_detail, name='order_detail'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),

]