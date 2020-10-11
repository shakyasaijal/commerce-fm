from django.conf import settings

from DashboardManagement.common import helper


def context_processor(request):
    context = {}
    try:
        if request.user.is_authenticated:
            user_permissions = helper.permission_of_current_user(request.user)
            context.update({'user_permissions': user_permissions})

            isVendorAdmin = False
            if settings.MULTI_VENDOR:
                if not request.user.is_superuser:
                    if helper.is_vendor_admin(request.user):
                        isVendorAdmin = True
                    context.update(
                        {'currentVendor': helper.current_user_vendor(request.user)})
            else:
                if request.user.is_superuser:
                    isVendorAdmin = True
                                            
            context.update({'is_vendor_admin': isVendorAdmin})

        context.update({'multi_vendor': settings.MULTI_VENDOR})
        context.update(
            {'has_additional_data': settings.HAS_ADDITIONAL_USER_DATA})
        context.update({'company_name': settings.COMPANY_NAME})

    except Exception as e:
        print(e)
    return context
