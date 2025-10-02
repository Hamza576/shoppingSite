from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from store.models import Product, Variation
from cart.models import Cart
from django.http import JsonResponse


def calculate_total_cart_cost(cart_products):
    total_amount = 0.0
    for item in cart_products:
        total_amount += item.product.price * item.quantity
    return total_amount


# Create your views here.
@login_required(login_url="login")
def add_to_cart(request):
    if request.method == "POST":
        product_id = request.POST["product_id"]
        color_variation = request.POST.get("color")
        size_variation = request.POST.get("size")
        product = Product.objects.get(id=product_id)

        # get selected variations
        selected_variations = []
        if color_variation:
            selected_variations.append(color_variation)
        if size_variation:
            selected_variations.append(size_variation)
        
        # Check if product already exists in cart for this user
        existing_cart_items = Cart.objects.filter(product=product_id, user=request.user)
        item_updated = False

        for cart_item in existing_cart_items:
            # Get all variations of this cart item
            cart_item_variations = cart_item.variations.all()
            existing_variations_in_cart = [item.variation_value for item in cart_item_variations]

            # If no variations were selected and cart item has no variations, they match
            if len(selected_variations) == 0 and len(existing_variations_in_cart) == 0:
                cart_item.quantity += 1
                cart_item.save()
                item_updated = True
                break
            # If variations were selected and they match exactly
            elif len(selected_variations) == len(existing_variations_in_cart) and set(selected_variations) == set(existing_variations_in_cart):
                cart_item.quantity += 1
                cart_item.save()
                item_updated = True
                break

        # If no matching cart item was found, create a new one
        if not item_updated:
            cart_item = Cart.objects.create(user=request.user, product=product, quantity=1)
            if selected_variations:
                variations = Variation.objects.filter(variation_value__in=selected_variations)
                cart_item.variations.set(variations)

        return redirect("show_cart")


@login_required(login_url="login")
def show_cart(request):
    current_user = request.user
    cart_items = Cart.objects.filter(user=current_user)

    cart_products = list(cart_items)  # convert queryset into list
    total_amount = calculate_total_cart_cost(cart_products)
    shipping_amount = 200.0

    context = {
        "cart_items": cart_items,
        "shipping_amount": shipping_amount,
        "total_amount": total_amount,
        "grand_total": total_amount + shipping_amount,
    }

    if len(cart_items) > 0:
        return render(request, "cart/cart.html", context)
    else:
        return render(request, "cart/emptycart.html", context)


def plus_cart(request):
    if request.method == "GET":
        product_id = request.GET["product_id"]
        cart_id = request.GET["cart_id"]
        cart_item = Cart.objects.get(id=cart_id, product=product_id, user=request.user)
        cart_item.quantity += 1
        cart_item.save()

        cart_items = Cart.objects.filter(user=request.user)
        total_amount = calculate_total_cart_cost(list(cart_items))
        shipping_amount = 200.0

        response = {
            "quantity": cart_item.quantity,
            "total_price": cart_item.total_price,
            "total_amount": total_amount,
            "grand_total": total_amount + shipping_amount,
        }

        if cart_item.quantity > 1:
            response["disabled"] = "false"

        return JsonResponse(response)


def minus_cart(request):
    if request.method == "GET":
        product_id = request.GET["product_id"]
        cart_id = request.GET["cart_id"]
        cart_item = Cart.objects.get(id=cart_id, product=product_id, user=request.user)

        cart_item.quantity -= 1
        cart_item.save()

        cart_items = Cart.objects.filter(user=request.user)
        total_amount = calculate_total_cart_cost(list(cart_items))
        shipping_amount = 200.0

        response = {
            "quantity": cart_item.quantity,
            "total_price": cart_item.total_price,
            "total_amount": total_amount,
            "grand_total": total_amount + shipping_amount,
        }

        if cart_item.quantity == 1:
            response["disabled"] = "true"

        return JsonResponse(response)


def remove_cart_item(request):
    if request.method == "GET":
        product_id = request.GET["product_id"]
        cart_id = request.GET["cart_id"]
        cart_item = Cart.objects.get(id=cart_id, product=product_id, user=request.user)
        cart_item.delete()

        cart_items = Cart.objects.filter(user=request.user)
        total_amount = calculate_total_cart_cost(list(cart_items))
        shipping_amount = 200.0

        response = {
            "total_amount": total_amount,
            "grand_total": total_amount + shipping_amount,
        }
        return JsonResponse(response)


def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)

    if len(cart_items) <= 0:
        return redirect("store")

    context = {
        "cart_items": cart_items,
    }

    return render(request, "store/checkout.html", context)



'''
if request.method == "POST":
        product_id = request.POST["product_id"]
        color_variation = request.POST.get("color")
        size_variation = request.POST.get("size")
        product = Product.objects.get(id=product_id)

        # before adding a product in cart, to check that product already exist in cart or not
        already_in_cart = Cart.objects.filter(
            product=product_id, user=request.user
        ).exists()

        if already_in_cart:
            cart_item = Cart.objects.get(product=product_id, user=request.user)
            # if the item exist in cart then get all the variations of that product
            cart_item_with_variations = cart_item.variations.all()
            # create a list of variations value
            existing_variations_in_cart = [
                item.variation_value for item in cart_item_with_variations
            ]
            # if the item exist in cart with same variations then increase the quantity of that product
            if (
                color_variation in existing_variations_in_cart
                and size_variation in existing_variations_in_cart
            ):
                cart_item.quantity += 1
                cart_item.save()
            # if the item exist in cart but user set different variations then add the product to cart
            elif (
                color_variation not in existing_variations_in_cart
                or size_variation not in existing_variations_in_cart
            ):
                cart_item = Cart.objects.create(
                    user=request.user, product=product, quantity=1
                )
                variations = Variation.objects.filter(
                    variation_value__in=[color_variation, size_variation]
                )
                cart_item.variations.set(variations)
        else:
            cart_item = Cart.objects.create(
                user=request.user, product=product, quantity=1
            )
            variations = Variation.objects.filter(
                variation_value__in=[color_variation, size_variation]
            )
            cart_item.variations.set(variations)

        return redirect("show_cart")
'''