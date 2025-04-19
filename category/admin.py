from django.contrib import admin
from category.models import Category

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_name', 'description', 'cat_image']
    prepopulated_fields = {"slug": ["category_name"]}
