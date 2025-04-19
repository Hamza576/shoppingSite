from django.urls import path
from cart import views

urlpatterns = [
    path('', views.show_cart, name='show_cart'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('plus-cart/', views.plus_cart),
    path('minus-cart/', views.minus_cart),
    path('remove-cart-item/', views.remove_cart_item),
    path('checkout/', views.checkout, name="checkout"),
]