import re
from django.conf import settings
from helper import modelHelper
from User import models as user_models
from CartSystem import models as cart_models



def create_group_validation(request):
    error = []
    try:
        if not request.POST['name']:
            error.append({'name': 'Group Name is required.'})
    except Exception as e:
        error.append({'name': 'Group Name is required.'})

    try:
        if not request.POST.getlist('to[]'):
            error.append(
                {'permissions': 'Permissions for the user are required.'})
    except Exception as e:
        error.append({'permissions': 'Permissions for the user are required.'})

    if error:
        return False, error
    else:
        return True, error


def create_vendor_user_validation(request, from_, id_=''):
    error = []
    collected_error = []
    try:
        if len(request.POST['first_name']) < 3:
            error.append(
                {'fn': 'Must be atleast 3 character long.'})
    except Exception as e:
        error.append({'fn': 'First Name is required.'})

    try:
        if len(request.POST['last_name']) < 3:
            error.append({'ln': 'Must be atleast 3 character long.'})
    except Exception as e:
        error.append({'ln': 'Last Name is required.'})

    # try:
    #     if not re.search(modelHelper.email_regex, request.POST['email']):
    #         error.append({'email': 'Email address is invalid.'})
    #         collected_error.append('email')
    # except Exception as e:
    #     error.append({'email': 'Email address is required.'})
    #     collected_error.append('email')

    try:
        if settings.HAS_ADDITIONAL_USER_DATA:
            if request.POST['phone']:
                int(request.POST['phone'])
    except (Exception) as e:
        if settings.HAS_ADDITIONAL_USER_DATA:
            if 'phone' not in collected_error:
                error.append({'phone': 'Invalid phone number.'})
                collected_error.append('phone')

    if from_ == "creation":
        try:
            user_models.User.objects.get(email=request.POST['email'])
            if 'email' not in collected_error:
                error.append({'email': 'Email already exists.'})
        except (Exception, user_models.User.DoesNotExist) as e:
            pass

        try:
            if settings.HAS_ADDITIONAL_USER_DATA:
                if request.POST['phone']:
                    user_models.UserProfile.objects.get(phone=request.POST['phone'])
                    if 'phone' not in collected_error:
                        error.append({'phone': 'Phone number already exists.'})
                        collected_error.append('phone')
        except (Exception, user_models.UserProfile.DoesNotExist) as e:
            pass

        try:
            patch = re.compile(modelHelper.password_reg)
            if not re.search(modelHelper.password_reg, request.POST['password']):
                error.append({'password': 'Password is invalid.'})
        except Exception as e:
            error.append({'password': 'Password is required.'})
    else:
        try:
            got = user_models.User.objects.get(email=request.POST['email'])
            if got.id is not id_:
                if 'email' not in collected_error:
                    error.append({'email': 'Email already exists.'})
        except (Exception, user_models.User.DoesNotExist) as e:
            pass

        try:
            if settings.HAS_ADDITIONAL_USER_DATA:
                if request.POST['phone']:
                    got = user_models.UserProfile.objects.get(phone=request.POST['phone'].strip())
                    if got.user.id != id_:
                        if 'phone' not in collected_error:
                            error.append({'phone': 'Phone number already exists.'})
                            collected_error.append('phone')
        except (Exception, user_models.UserProfile.DoesNotExist) as e:
            pass
            print(e)
    

    try:
        if settings.HAS_ADDITIONAL_USER_DATA:
            if request.POST['phone']:
                if len(request.POST['phone']) < 7:
                    if 'phone' not in collected_error:
                        error.append({'phone': 'Must be atleast 7 digit long.'})
                        collected_error.append('phone')
    except Exception as e:
        pass
    

    
    try:
        if settings.HAS_ADDITIONAL_USER_DATA:
            if request.POST['district']:
                if not cart_models.Location.objects.get(id=request.POST['district']):
                    if 'location' not in collected_error:
                        error.append({'location': 'Location not found.'})
                        collected_error.append('location')
    except (Exception, cart_models.Location.DoesNotExist) as e:
        pass

    if error:
        return False, error
    else:
        return True, error
