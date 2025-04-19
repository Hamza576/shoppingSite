from cart.models import Cart


def cart_items_count(request):
    cart_items = Cart.objects.all()

    total_cart_items = 0
    for cart_item in cart_items:
        total_cart_items += cart_item.quantity

    return {"total_cart_items": total_cart_items}
