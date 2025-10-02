from django.shortcuts import render, redirect
from accounts.forms import RegistrationForm, LoginForm, PasswordResetForm, UserForm, UserProfileForm
from django.contrib import messages
from django.conf import settings
from accounts.models import User, UserProfile
from order.models import Order, OrderProduct
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

# Sending email
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from accounts.utils import send_activation_email, send_reset_password_email


# Create your views here.
def registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            # send email for account activation
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            # activation_link = f"{settings.SITE_DOMAIN}/activate/{uid}/token/"
            activation_link = reverse(
                "activate", kwargs={"uidb64": uidb64, "token": token}
            )
            activation_url = f"{settings.SITE_DOMAIN}{activation_link}"
            send_activation_email(user.email, activation_url)
            messages.success(request, "Account Created Successfully!")
            messages.success(
                request,
                "We have sent an email to your inbox. Please, Check email to activate your account.",
            )
            return redirect("login")
    else:
        form = RegistrationForm()
    return render(request, "accounts/register.html", {"form": form})


def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(force_str(uidb64))
        user = User.objects.get(pk=uid)

        if user.is_active:
            messages.warning(request, "Your account is already activated!")
            return redirect("login")

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(
                request,
                "Your account has been Successfully Activated! Now you can Login",
            )
            return redirect("login")
        else:
            messages.error(request, "The Activation Link is Invalid or has Expired.", extra_tags='danger')
            return redirect("login")

    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
        messages.error(request, "Activation Link is Invalid!", extra_tags='danger')
        return redirect("login")

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login Successfully!")
                return redirect('dashboard')
            else:
                messages.error(request, "Not Logged In!", extra_tags='danger')
    else:
        form = LoginForm()
    return render(request, "accounts/signin.html", {"form": form})

def password_reset_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.filter(email=email).first()
            if user:
                # send email for reset password
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_link = reverse(
                    "password_reset_confirm", kwargs={"uidb64": uidb64, "token": token}
                )
                reset_url = f"{settings.SITE_DOMAIN}{reset_link}"
                send_reset_password_email(user.email, reset_url)
                messages.success(request, "We have sent an Password Reset link. Please check your Email Inbox!")
                return redirect('login')
    else:
        form = PasswordResetForm()
    return render(request, "accounts/password_reset.html", {'form': form})

def password_reset_confirm_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(force_str(uidb64))
        user = User.objects.get(pk=uid)

        if default_token_generator.check_token(user, token):
            if request.method == 'POST':
                form = SetPasswordForm(user, request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Your Password has been successfully Reset!")
                    return redirect('login')
            else:
                form = SetPasswordForm(user)

            return render(request, 'account/password_reset_confirm.html', {'form': form})
        else:
            messages.error(request, "The Password Reset Link is Invalid or has Expired.", extra_tags='danger')
            return redirect('password_reset')

    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
        messages.error(request, "Link has Expired or is Invalid!", extra_tags='danger')
        return redirect("password_reset")
    
@login_required(login_url="login")
def dashboard_view(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True)
    total_orders = orders.count()
    # user_phone = Order.objects.filter(user=request.user)[0].phone

    context = {
        'orders': orders,
        'total_orders': total_orders,
        'user_phone': '123232323',
    }
    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url="login")
def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    order_count = orders.count()

    context = {
        'orders': orders,
        'order_count': order_count,
    }
    return render(request, 'accounts/my_orders.html', context)

@login_required(login_url="login")
def order_detail(request, order_number):
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        products = OrderProduct.objects.filter(order__order_number=order_number)

        sub_total = 0.0
        for product in products:
            sub_total += product.product.price * product.quantity
    except Order.DoesNotExist:
        return redirect('my_orders')

    context = {
        'order': order,
        'products': products,
        'sub_total': sub_total,
    }
    return render(request, 'accounts/order_detail.html', context)

@login_required(login_url="login")
def edit_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile has been updated successfully!")
            return redirect('edit_profile')

    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'accounts/user_profile.html', context)


@login_required(login_url="login")
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user) # restrict the django default behavior to logout the user
            messages.success(request, "Password has been Changed Successfully!")
            return redirect('change_password')
    else:
        form = PasswordChangeForm(user=request.user)
    
    context = {
        'form': form,
    }
    return render(request, 'accounts/password_change.html', context)
