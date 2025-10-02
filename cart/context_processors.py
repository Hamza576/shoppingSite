from cart.models import Cart

def cart_items_count(request):
    total_cart_items = 0
    if request.user.is_authenticated:
        current_user = request.user # get logged-in user
        cart_items = Cart.objects.filter(user=current_user) # get cart items of current user

        for cart_item in cart_items:
            total_cart_items += cart_item.quantity

    return {"total_cart_items": total_cart_items}
