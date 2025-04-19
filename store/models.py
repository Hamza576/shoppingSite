from django.db import models
from category.models import Category
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    image = models.ImageField(upload_to="images/product")
    stock = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # generate product url based on category slug and product slug
    def get_url(self):
        return reverse(
            "product-detail-view",
            kwargs={"category_slug": self.category.slug, "product_slug": self.slug},
        )

    def __str__(self):
        return self.product_name


variation_category_choices = [
    ("color", "color"),
    ("size", "size"),
]


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(
        choices=variation_category_choices, max_length=100
    )
    variation_value = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.variation_value