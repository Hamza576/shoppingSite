from django.db import models
from accounts.models import User
from store.models import Product, Variation


# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    variations = models.ManyToManyField(Variation, blank=True)

    @property
    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self) -> str:
        return self.product.product_name
