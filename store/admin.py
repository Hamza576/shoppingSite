from django.contrib import admin
from store.models import Product, Variation


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "product_name",
        "price",
        "image",
        "stock",
        "category",
        "is_available",
    ]
    prepopulated_fields = {"slug": ["product_name"]}


@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = ["id", "product", "variation_category", "variation_value", "is_active"]
    list_editable = ["is_active"]
