from django.contrib.auth.models import Group
from django.conf import settings

from DashboardManagement.common import helper as app_helper
from CartSystem import models as cart_models
from User import models as user_models


def create_vendor_user(request, vendor):
    user = user_models.User.objects.none()
    try:
        user = user_models.User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], username=request.POST['email'])
        user_models.UserProfile.objects.create(user=user, phone=request.POST['phone'], address=request.POST['address'], district=cart_models.Location.objects.get(id=request.POST['district']))
        user.set_password(request.POST['password'])
        user.save()

        # Add to Group
        if request.POST.getlist('groups'):
            for data in request.POST.getlist('groups'):
                Group.objects.get(id=data).user_set.add(user)

        # Add district
        try:
            if request.POST['district']:
                user.location = api_models.Location.objects.get(id=request.POST['district'])
                user.save()
        except Exception as e:
            pass

        if settings.MULTI_VENDOR:
            # Add to vendor
            vendor = app_helper.current_user_vendor(request.user)
            vendor.vendorUsers.add(user)

    except Exception as e:
        print(e)
        if user:
            user.delete()
        return False
    return True