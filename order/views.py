import datetime
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from order.forms import OrderForm
from order.models import Order, Payment, OrderProduct
from cart.models import Cart
from cart.views import calculate_total_cart_cost
import json
from accounts.utils import send_order_received_email

# Create your views here.
@login_required(login_url='login')
def payment(request):
    body = json.loads(request.body) # convert json data into python dictionary
    current_user = request.user
    order = Order.objects.get(user=current_user, is_ordered=False, order_number=body['orderNumber'])
    cart_items = Cart.objects.filter(user=current_user)

    # when payment is successful then we store the payment data into table 
    payment = Payment.objects.create(user=current_user, payment_id=body['transactionId'], payment_method=body['paymentMethod'], amount_paid=order.order_total, status=body['status'])

    # when payment is successful then we update the order table fields
    order.payment = payment
    order.is_ordered = True
    order.save()

    # when payment is successful then we move the cart products into orderProduct table
    for cart_item in cart_items:
        order_product = OrderProduct.objects.create(order=order, payment=payment, user=current_user, product=cart_item.product, quantity=cart_item.quantity, product_price=cart_item.total_price, ordered=True)

        prod_variations = cart_item.variations.all()
        order_product.variations.set(prod_variations)

        # and reduce the stock when order is successful
        cart_item.product.stock -= cart_item.quantity
        cart_item.product.save()

    # and at the end remove all products from cart
    cart_items.delete()

    # send order recieved email to customer 
    order = Order.objects.get(user=current_user, order_number=body['orderNumber'], is_ordered=True)
    send_order_received_email(order.email, order.order_number)

    # send order number and transaction id back to sendData method from where request is coming
    data = {
        'order_number': order.order_number,
        'transaction_id': payment.payment_id,
    }

    return JsonResponse(data)


@login_required(login_url='login')
def place_order(request):
    current_user = request.user
    cart_items = Cart.objects.filter(user=current_user)

    grand_total = 0.0
    total_amount = calculate_total_cart_cost(list(cart_items))
    shipping_amount = 200.0
    grand_total = total_amount + shipping_amount

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # store billing information into Order table
            order = Order() # create instance of Order class
            order.user = current_user
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']
            order.address = form.cleaned_data['address']
            order.city = form.cleaned_data['city']
            order.state = form.cleaned_data['state']
            order.country = form.cleaned_data['country']
            order.order_note = form.cleaned_data['order_note']
            order.shipping_amount = shipping_amount
            order.order_total = grand_total
            order.ip_address = request.META.get('REMOTE_ADDR') # get the ip addresss
            order.save()
            # generate unique order id
            id = datetime.datetime.now().strftime('%Y%m%d')
            order_number = id + str(order.pk)
            order.order_number = order_number
            order.save()

            user_order = Order.objects.get(user=current_user, order_number=order_number,is_ordered=False)
            context = {
                'order': user_order,
                'total_amount': total_amount,
                'shipping_amount': shipping_amount,
                'grand_total': grand_total,
                'cart_items': cart_items,
            }
            return render(request, 'orders/payment.html', context)
    else:
        return redirect('checkout')

def order_complete(request):
    order_number = request.GET.get('order_number')
    payment_id = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        payment = Payment.objects.get(payment_id=payment_id)
        products = OrderProduct.objects.filter(user=request.user, payment=payment)

        # calculate sub_total of products
        sub_total = 0.0
        for product in products:
            sub_total += product.product.price * product.quantity
    except (Order.DoesNotExist, Payment.DoesNotExist):
        return redirect('home')
    
    context = {
        'order': order,
        'payment': payment,
        'products': products,
        'sub_total': sub_total,
    }

    return render(request, 'orders/order_complete.html', context)