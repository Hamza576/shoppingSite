from django.shortcuts import render, redirect
from store.models import Product, Variation
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

# Create your views here.
def store(request, single_category=None):
    low_price = request.GET.get('low-price')
    high_price = request.GET.get('high-price')
    categories = request.GET.getlist('category')
    
    products = Product.objects.filter(is_available=True).order_by('created_at')

    if low_price and high_price:
        if low_price > high_price:
            # messages.error(request, f'{low_price} is greater than {high_price}')
            # return redirect('store')
            pass
        products = products.filter(price__range=(low_price, high_price))
    if single_category:
        products = products.filter(category__slug=single_category)
    if categories:
        products = products.filter(category__slug__in=categories).distinct()

    paginator = Paginator(products, 6) # show 6 produts per page
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(paginator.num_pages)
    except EmptyPage:
        page_obj = paginator.page(1)


    product_count = len(page_obj) # count length of products on each page

    context = {
        "products": page_obj,
        "product_count": product_count,
        'low_price': low_price,
        'high_price': high_price,
        'selected_categories': request.GET.getlist('category')
    }

    return render(request, "store/store.html", context)

def product_detail_view(request, category_slug, product_slug):
    try:
        product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Product.DoesNotExist:
        pass
    
    color_variations = Variation.objects.filter(product=product, variation_category='color', is_active=True)
    size_variations = Variation.objects.filter(product=product, variation_category='size', is_active=True)

    context = {
        'product': product,
        'color_variations': color_variations,
        'size_variations': size_variations,
    }
    return render(request, 'store/product-detail.html', context)


def search(request):
    keyword = request.GET.get('keyword')
    if not keyword.strip():
        return redirect('home')
    
    if keyword:
        products = Product.objects.filter(Q(product_name__icontains=keyword)|Q(description__icontains=keyword))        
        product_count = products.count()
    
    context = {
        'products': products,
        'product_count': product_count,
        'keyword': keyword,
        'all': request.GET.items(),
    }
    return render(request, "store/store.html", context)
 
