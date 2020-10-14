import datetime
from django.conf import settings
from celery import shared_task
from django.core.mail import send_mail, BadHeaderError, EmailMessage
import socket
import smtplib
from django.template.loader import render_to_string

from Referral import models as refer_models
from Referral import utils


def participate_on_chain_of_referral(user, request):
    referredBy = refer_models.Referral.objects.none()
    flag = False

    '''
    If referCode is passed from frontend
    '''
    try:
        referredBy = refer_models.Referral.objects.get(
            refer_code=request.data['referCode'])
        flag = True
    except (Exception, refer_models.Referral.DoesNotExist, refer_models.Reward.DoesNotExist):
        pass

    '''
    If referCode is not passed, then check with uik
    '''
    if not flag:
        try:
            by_uik = refer_models.UserKey.objects.get(
                key=request.data['__uik'])
            referredBy = by_uik.referredFrom
            flag = True
        except (Exception, refer_models.UserKey.DoesNotExist):
            pass

    '''
    If referCode and uik is not passed, then generate uik with same process
    then check if it is found in database.

    > If found in database, return its referredBy
    '''
    if not flag:
        try:
            agent_data = utils.user_agent_data(request)
            agent_data.update({"ip": utils.get_ip(request)})
            key = utils.generate_refered_user_key(agent_data, "user")
            refer_instance = refer_models.UserKey.objects.get(key=key)
            referredBy = refer_instance.referredFrom
            flag = True
        except (Exception, refer_models.UserKey.DoesNotExist):
            pass

    if flag:
        reward = refer_models.Reward.objects.get(referral=referredBy)
        reward.signed_up = reward.signed_up+1
        reward.save()
        try:
            block_of_referral = refer_models.Block.objects.get(
                user=referredBy.user)
            # Block Chain for tracking
            data = {
                "userId": user.id,
                "email": user.email,
                "timestamp": datetime.datetime.timestamp(datetime.datetime.now())
            }
            genesis = False
            data_hash = utils.hash_data(str(data))
            refer_models.Block.objects.create(
                data=data, data_hash=data_hash, previous_hash=block_of_referral.data_hash, genesis_block=genesis)
            return True, referredBy
        except (Exception, refer_models.Block.DoesNotExist):
            pass
    return False, ''


def change_password(request):
    err = None

    if not request.data['newPassword'] == request.data['confirmPassword']:
        err = "Passwords do not match."
        return err

    if len(request.data['newPassword']) < 8:
        err = "Password must be atleast 8 characters long."
        return err

    if request.data['newPassword'] == request.data['oldPassword']:
        err = "New password should be different than old password."
        return err

    return err


@shared_task
def password_changed_email_with_delay(subject, data):
    print("came")
    try:
        sender = settings.EMAIL_HOST_USER
        password = settings.EMAIL_HOST_PASSWORD
        recipient = data['email']
        context = {
            'full_name': data['full_name'],
            'company_name': settings.COMPANY_NAME,
            'osFamily': data['osFamily'],
            'osVersion': data['osVersion'],
            'deviceFamily': data['deviceFamily'],
            'deviceBrand': data['deviceBrand'],
            'datetime': datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
        update_details = render_to_string(
            'change_password_email.html', context)

        msg = EmailMessage(subject, update_details, '{} {}'.format(
            settings.COMPANY_NAME, sender), [recipient])
        msg.content_subtype = "html"
        msg.send()
    except (BadHeaderError, socket.gaierror, smtplib.SMTPException, Exception) as e:
        print(e)
        return False
    return True


def password_changed_email_without_delay(subject, data):
    try:
        sender = settings.EMAIL_HOST_USER
        password = settings.EMAIL_HOST_PASSWORD
        recipient = data['email']
        context = {
            'full_name': data['full_name'],
            'company_name': settings.COMPANY_NAME,
            'osFamily': data['osFamily'],
            'osVersion': data['osVersion'],
            'deviceFamily': data['deviceFamily'],
            'deviceBrand': data['deviceBrand'],
            'datetime': datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
        update_details = render_to_string(
            'change_password_email.html', context)

        msg = EmailMessage(subject, update_details, '{} {}'.format(
            settings.COMPANY_NAME, sender), [recipient])
        msg.content_subtype = "html"
        msg.send()
    except (BadHeaderError, socket.gaierror, smtplib.SMTPException, Exception) as e:
        print(e)
        return False
    return True


def complete_profile(request):
    err = None

    if not request.data['phone'].strip() or not request.data['address'].strip() or not request.data['district'].strip():
        err = "All fields are required."
        return err
    return err
