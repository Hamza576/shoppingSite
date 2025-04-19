from django.contrib import admin
from order.models import Payment, Order, OrderProduct


# Register your models here.
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "payment_method", "amount_paid", "status"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "payment",
        "first_name",
        "phone",
        "email",
        "city",
        "country",
        "order_total",
        "status",
        "created_at",
        "is_ordered",
    ]


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "order",
        "payment",
        "user",
        "product",
        "quantity",
        "product_price",
        "ordered",
        "created_at",
    ]
