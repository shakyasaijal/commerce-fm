from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.conf import settings

from Vendor import models as vendor_models
from Referral import models as refer_models


def excluding_permissions():
    excludable_models_for_permissions = []
    try:
        excludable_models_for_permissions.append(
            ContentType.objects.get(model='LogEntry'))
    except Exception as e:
        pass
    try:
        excludable_models_for_permissions.append(
            ContentType.objects.get(model='Location'))
    except Exception as e:
        pass

    try:
        excludable_models_for_permissions.append(
            ContentType.objects.get(model='marketing'))
    except Exception as e:
        pass

    try:
        excludable_models_for_permissions.append(
            ContentType.objects.get(model='session'))
    except Exception as e:
        pass
    try:
        excludable_models_for_permissions.append(
            ContentType.objects.get(model='tags'))
    except Exception as e:
        pass

    try:
        excludable_models_for_permissions.append(
            ContentType.objects.get(model='addtocart'))
    except Exception as e:
        pass

    try:
        excludable_models_for_permissions.append(
            ContentType.objects.get(model='brand'))
    except Exception as e:
        pass

    try:
        excludable_models_for_permissions.append(
            ContentType.objects.get(model='size'))
    except Exception as e:
        pass

    return excludable_models_for_permissions


def permissions_of_group(group):
    excludable_models_for_permissions = excluding_permissions()
    permissions = group.permissions.exclude(
        content_type_id__in=excludable_models_for_permissions).order_by('id')
    return permissions


def is_vendor_admin(user):
    vendors = vendor_models.Vendor.objects.all()
    for vendor in vendors:
        if user == vendor.vendorAdmin:
            return True

    return False


def access_to_vendor(user):
    vendors = vendor_models.Vendor.objects.all()
    for vendor in vendors:
        if user in vendor.vendorUsers.all() or user == vendor.vendorAdmin:
            return True

    return False


def current_user_vendor(user):
    for vendor in vendor_models.Vendor.objects.all():
        if user == vendor.vendorAdmin or user in vendor.vendorUsers.all():
            return vendor


def vendor_of_a_user(user):
    for vendor in vendor_models.Vendor.objects.all():
        if user in vendor.vendorUsers.all():
            return vendor


def permission_of_current_user(user):
    permissions = []

    for data in Permission.objects.filter(group__user=user).order_by('-content_type'):
        permissions.append(data.codename)

    return permissions


def get_all_groups_of_a_vendor(user):
    vendor = current_user_vendor(user)
    grp = Group.objects.filter(vendor=vendor)

    return grp


def access_management(permission, request):
    isOK = True
    if settings.MULTI_VENDOR:
        if not request.user.has_perm(permission) and not is_vendor_admin(request.user):
            isOK = False
    else:
        if not request.user.has_perm(permission) or not request.user.is_superuser:
            isOK = False

    return isOK


def childBlocks(block):
    hash_key = block.data_hash
    count = 0

    try:
        while refer_models.VendorBlock.objects.filter(previous_hash=hash_key):
            block = refer_models.VendorBlock.objects.filter(
                previous_hash=hash_key)[0]
            hash_key = block.data_hash
            count += 1
    except (Exception, refer_models.VendorBlock.DoesNotExist) as e:
        print(e)

    return count
