from django.conf import settings
from datetime import datetime, timedelta
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from celery import shared_task
import smtplib
import socket
from django.template.loader import render_to_string


@shared_task
def send_email_with_delay(subject, data):
    try:
        sender = settings.EMAIL_HOST_USER
        password = settings.EMAIL_HOST_PASSWORD
        recipient = data['email']
        current_site = data['current_site']
        exp = str(datetime.now() + timedelta(hours=1))
        context = {
            'full_name': data['full_name'],
            'domain': data['current_site'],
            'secure': data['secure'],
            'from': data['from'],
            'company_name': settings.COMPANY_NAME
        }
        if subject == "Vendor Registration":
            update_details = render_to_string('vendor-registration.html',context)
        elif subject == "Password Reset":
            update_details = render_to_string('reset_password.html',context)
        elif subject == "Password Reset Request":
            update_details = render_to_string('web_reset_password.html',context)

        msg = EmailMessage(subject, update_details, '{} {}'.format(settings.COMPANY_NAME, sender), [recipient])
        msg.content_subtype = "html" 
        msg.send()
    except (BadHeaderError, socket.gaierror, smtplib.SMTPException, Exception) as e:
        print(e)
        return False
    return True


def send_email_without_delay(subject, data):
    try:
        sender = settings.EMAIL_HOST_USER
        password = settings.EMAIL_HOST_PASSWORD
        recipient = data['email']
        current_site = data['current_site']
        exp = str(datetime.now() + timedelta(hours=1))
        context = {
            'full_name': data['full_name'],
            'domain': data['current_site'],
            'secure': data['secure'],
            'from': data['from'],
            'company_name': settings.COMPANY_NAME
        }
        if subject == "Vendor Registration":
            update_details = render_to_string('vendor-registration.html',context)
        elif subject == "Password Reset":
            update_details = render_to_string('reset_password.html',context)
        elif subject == "Password Reset Request":
            update_details = render_to_string('web_reset_password.html',context)

        msg = EmailMessage(subject, update_details, '{} {}'.format(settings.COMPANY_NAME, sender), [recipient])
        msg.content_subtype = "html" 
        msg.send()
    except (BadHeaderError, socket.gaierror, smtplib.SMTPException, Exception) as e:
        print(e)
        return False
    return True
