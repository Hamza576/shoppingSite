from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def send_activation_email(recipient_email, activation_url):
    subject = "Activate Your Account on " + settings.SITE_NAME
    from_email = "no_reply@demomailtrap.co"
    to_email = [recipient_email]

    # Render html content
    html_content = render_to_string(
        "accounts/account_activation_email.html", {"activation_url": activation_url}
    )
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=True)

def send_reset_password_email(recipient_email, reset_url):
    subject = "Reset Your Password on " + settings.SITE_NAME
    from_email = "no_reply@demomailtrap.co"
    to_email = [recipient_email]

    # Render html content
    html_content = render_to_string(
        "accounts/password_reset_email.html", {"reset_url": reset_url}
    )
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=True)

def send_order_received_email(recipient_email, order_number):
    subject = "Thanks for Purchasing on " + settings.SITE_NAME
    from_email = "no_reply@demomailtrap.co"
    to_email = [recipient_email]

    # Render html content
    html_content = render_to_string(
        "orders/order_received_email.html", {"order_number": order_number}
    )
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=True)
