from django.urls import path
from store import views

urlpatterns = [
    path('', views.store, name='store'),
    path('product-detail/<slug:category_slug>/<slug:product_slug>/', views.product_detail_view, name='product-detail-view'),
    path('search/', views.search, name='search'),
]