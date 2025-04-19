from django.shortcuts import render
from store.models import Product

def home(rqeuest):
    products = Product.objects.filter(is_available=True)

    context = {
        'products': products,
    }
    return render(rqeuest, 'home.html', context)