from category.models import Category

def category_list(request):
    category_links = Category.objects.all()

    return {'category_links': category_links}