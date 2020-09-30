from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.contrib.auth.models import Group
from django.db.models import Q, Count, Sum
from collections import Counter 


from DashboardManagement.views import vendor_only
from DashboardManagement.common import routes as navbar
from Vendor import models as vendor_models
from Vendor import forms as vendor_forms
from User import models as user_models
from CartSystem import models as cart_models
from DashboardManagement.common import emails as send_email
from OrderAndDelivery import models as order_models
from Products import models as product_models
from Analytics import views as analytics_views


template_version = "DashboardManagement/v1"
try:
    if settings.TEMPLATE_VERSION:
        template_version = "DashboardManagement/"+settings.TEMPLATE_VERSION
except Exception:
    pass


class VendorsList(LoginRequiredMixin, View):
    def common(self, request):
        context = {}
        all_vendors = vendor_models.Vendor.objects.all()
        pending_vendors = vendor_models.VendorRequest.objects.all()
        routes = navbar.get_formatted_routes(navbar.get_routes(
            request.user), active_page='vendor management')
        context.update({"routes": routes})
        context.update({"title": "Vendor Management"})
        context.update({"sub_navbar": "vendors"})
        context.update({"all_vendors": all_vendors})
        context.update({"pending_vendors": pending_vendors})
        return context

    def get(self, request):
        if not request.user.is_superuser:
            messages.error(request, 'You do not have permission.')
            return HttpResponseRedirect(reverse('vendor-home'))
        routes = navbar.get_formatted_routes(navbar.get_routes(
            request.user), active_page='vendor management')

        context = {}
        context.update(self.common(request))
        if request.method == 'GET':
            form = vendor_forms.VendorRequestForm()
            context.update({"form": form})
        return render(request, template_version+"/Views/VendorView/index.html", context=context)

    def post(self, request):
        form = vendor_forms.VendorRequestForm(request.POST)
        try:
            user_models.User.objects.get(email=request.POST['email'])
            messages.warning(request, "User with that email already exists.")
            return HttpResponseRedirect(reverse('vendor-vendors'))
        except (Exception, user_models.User.DoesNotExist):
            pass

        try:
            vendor_models.VendorRequest.objects.get(
                email=request.POST['email'])
            messages.warning(request, "Vendor with that email already exists.")
            return HttpResponseRedirect(reverse('vendor-vendors'))
        except (Exception, vendor_models.VendorRequest.DoesNotExist):
            pass

        if form.is_valid():
            form.save()
            email_data = {
                "current_site": get_current_site(request).domain,
                "secure": request.is_secure() and "https" or "http",
                "email": request.POST["email"],
                "from": request.user.get_full_name(),
                "full_name": "{} {}".format(request.POST["first_name"], request.POST["last_name"])
            }
            flag = False
            if settings.CELERY_FOR_EMAIL:
                if send_email.send_email_with_delay.delay("Vendor Registration", email_data):
                    flag = True
            else:
                if send_email.send_email_without_delay("Vendor Registration", email_data):
                    flag = True
            if not flag:
                try:
                    vendor = vendor_models.VendorRequest.objects.get(
                        email=request.POST['email'])
                    vendor.delete()
                except (Exception, vendor_models.VendorRequest.DoesNotExist):
                    pass
                messages.error(
                    request, "Vendor email is not valid. Please try again.")
            else:
                messages.success(
                    request, "Vendor has been successfully added.")

            return HttpResponseRedirect(reverse('vendor-vendors'))
        else:
            context = {}
            context.update(self.common(request))
            context.update({"form": form})
            return render(request, template_version+"/Views/VendorView/index.html", context=context)


class JoinAsVendor(View):
    def get(self, request):
        # if request.user.is_authenticated:
        #     messages.warning(request, "You are already logged in.")
        #     return HttpResponseRedirect(reverse('index'))
        return render(request, template_version+"/Views/VendorView/join.html")

    def post(self, request):
        # if request.user.is_authenticated:
        #     messages.warning(request, "You are already logged in.")
        #     return HttpResponseRedirect(reverse('index'))
        try:
            vendor = vendor_models.VendorRequest.objects.get(
                email=request.POST['email'])
            districts = cart_models.Location.objects.all()
            return render(request, template_version+"/Views/VendorView/register.html", {"email": request.POST['email'], "vendor": vendor, "districts": districts})
        except (Exception, vendor_models.VendorRequest.DoesNotExist) as e:
            print(e)
            messages.error(request, "Invalid email address. Please try again.")
            return HttpResponseRedirect(reverse('vendor-join'))


def validate_register(request):
    error = []
    error_listed = []

    if len(request.POST['password']) < 8:
        error.append(
            {"for": "password", "error": "Password must be 8 character long."})
        error_listed.append("password")

    if request.POST['password'] != request.POST['confirm_password']:
        error.append(
            {"for": "password", "error": "Two password does not match."})
        error_listed.append("password")

    try:
        cart_models.Location.objects.get(id=request.POST['district'])
    except (Exception, cart_models.Location.DoesNotExist):
        error.append({"for": "district", "error": "District not found."})
        error_listed.append("district")

    if len(request.POST['address']) <= 0:
        error.append({"for": "address", "error": "Address is required."})
        error_listed.append("address")

    if len(request.POST['phone']) <= 0:
        error.append({"for": "phone", "error": "Phone number is required."})
        error_listed.append("phone")

    try:
        int(request.POST['phone'])
    except Exception:
        if "phone" not in error_listed:
            error.append({"for": "phone", "error": "Invalid phone number"})

    if error:
        return True, error

    return False, error


class RegisterAsVendor(View):
    def get(self, request):
        return HttpResponseRedirect(reverse('vendor-join'))

    def post(self, request):
        try:
            vendor = vendor_models.VendorRequest.objects.get(
                email=request.POST['vendor_email'])
            districts = cart_models.Location.objects.all()
            error = validate_register(request)
            if not error[0]:
                try:
                    new_user = user_models.User.objects.create(
                        first_name=vendor.first_name, last_name=vendor.last_name, username=request.POST['vendor_email'], email=request.POST['vendor_email'])
                    new_user.set_password(request.POST['password'])
                    new_user.save()
                except Exception as e:
                    print("New User ", e)
                    messages.error(
                        request, "Something went wrong. Please try again.")
                    return HttpResponseRedirect(reverse('vendor-join'))

                if new_user:
                    try:
                        new_profile = user_models.UserProfile.objects.create(user=new_user, district=cart_models.Location.objects.get(
                            id=request.POST['district']), phone=request.POST['phone'], address=request.POST['address'])
                    except (Exception, cart_models.Location.DoesNotExist) as e:
                        print("New Profile ", e)
                        if new_user:
                            new_user.delete()
                        messages.error(request, "")
                if new_user and new_profile:
                    try:
                        new_vendor = vendor_models.Vendor.objects.create(
                            organizationName=vendor.organizationName, address=request.POST['address'], vendorAdmin=new_user)
                    except Exception as e:
                        print("New Vendor ", e)
                        if new_user:
                            new_user.delete()
                        if new_profile:
                            new_profile.delete()

                if new_user and new_profile and new_vendor:
                    vendor.delete()
                    messages.success(request, "Welcome, {}".format(
                        new_user.get_full_name()))
                    auth = authenticate(
                        request, username=new_user.email, password=request.POST['password'])
                    login(request, auth)
                    return HttpResponseRedirect(reverse('vendor-home'))
                else:
                    messages.error(
                        request, "Something went wrong. Please try again.")
                    return HttpResponseRedirect(reverse('vendor-join'))
            else:
                return render(request, template_version+"/Views/VendorView/register.html", {"email": request.POST['vendor_email'], "vendor": vendor, "districts": districts, "error": error[1]})

            return render(request, template_version+"/Views/VendorView/register.html", {"email": request.POST['email'], "vendor": vendor, "districts": districts})
        except (Exception, vendor_models.VendorRequest.DoesNotExist) as e:
            print(e)
            messages.error(request, "Invalid email address. Please try again.")
            return HttpResponseRedirect(reverse('vendor-join'))


class DeleteVendorRequest(LoginRequiredMixin, View):
    def post(self, request):
        if not request.user.is_superuser:
            messages.error(request, "You do not have permission.")
            return HttpResponseRedirect(reverse('vendor-home'))

        try:
            vendor = vendor_models.VendorRequest.objects.get(
                id=request.POST['vr-id'])
            vendor.delete()
            messages.success(request, "Vendor has been successfully delete.")
        except (Exception, vendor_models.VendorRequest.DoesNotExist) as e:
            messages.error(request, "Data not found.")

        return HttpResponseRedirect(reverse('vendor-vendors'))


class EditVendorRequest(LoginRequiredMixin, View):
    def post(self, request):
        if not request.user.is_superuser:
            messages.error(request, "You do not have permission.")
            return HttpResponseRedirect(reverse('vendor-home'))

        try:
            vendor = vendor_models.VendorRequest.objects.get(
                id=request.POST['vr-id'])
            if vendor.email != request.POST['email']:
                try:
                    vendor_models.VendorRequest.objects.get(
                        email=request.POST['email'])
                    user_models.User.objects.get(email=request.POST['email'])
                    messages.warning(
                        request, "User with this email already exists.")
                    return HttpResponseRedirect(reverse('vendor-vendors'))
                except (Exception, vendor_models.VendorRequest.DoesNotExist, user_models.User.DoesNotExist):
                    vendor.email = request.POST['email']

            vendor.organizationName = request.POST['organizationName']
            vendor.first_name = request.POST['first_name']
            vendor.last_name = request.POST['last_name']
            vendor.save()
            if request.POST.getlist('send_email_again'):
                email_data = {
                    "current_site": get_current_site(request).domain,
                    "secure": request.is_secure() and "https" or "http",
                    "email": vendor.email,
                    "from": request.user.get_full_name(),
                    "full_name": "{} {}".format(vendor.first_name, vendor.last_name)
                }
                flag = False
                if settings.CELERY_FOR_EMAIL:
                    if send_email.send_email_with_delay.delay("Vendor Registration", email_data):
                        flag = True
                else:
                    if send_email.send_email_without_delay("Vendor Registration", email_data):
                        flag = True
                if not flag:
                    messages.error(
                        request, "Vendor email is not valid. Please try again.")
                else:
                    messages.success(request, "Vendor Successfully Updated.")
            else:
                messages.success(request, "Vendor Successfully Updated.")
        except (Exception, vendor_models.VendorRequest.DoesNotExist) as e:
            messages.error(request, "Data not found.")

        return HttpResponseRedirect(reverse('vendor-vendors'))


class ResendRegistrationEmail(LoginRequiredMixin, View):
    def get(self, request, id):
        if not request.user.is_superuser:
            messages.error(request, "You do not have permission.")
            return HttpResponseRedirect(reverse('vendor-home'))

        try:
            vendor = vendor_models.VendorRequest.objects.get(id=id)
            email_data = {
                "current_site": get_current_site(request).domain,
                "secure": request.is_secure() and "https" or "http",
                "email": vendor.email,
                "from": request.user.get_full_name(),
                "full_name": "{} {}".format(vendor.first_name, vendor.last_name)
            }

            flag = False
            if settings.CELERY_FOR_EMAIL:
                if send_email.send_email_with_delay.delay("Vendor Registration", email_data):
                    flag = True
            else:
                if send_email.send_email_without_delay("Vendor Registration", email_data):
                    flag = True
            if not flag:
                messages.error(
                    request, "Vendor email is not valid. Please try again.")
            else:
                messages.success(request, "Email has been resend.")

        except (Exception, vendor_models.VendorRequest.DoesNotExist) as e:
            messages.error(request, "Data not found.")

        return HttpResponseRedirect(reverse('vendor-vendors'))


class VendorDetails(LoginRequiredMixin, View):
    def get(self, request, id):
        if not request.user.is_superuser:
            messages.warning(request, "You do not have permission.")
            return HttpResponseRedirect(reverse('vendor-home'))

        try:
            vendor = vendor_models.Vendor.objects.get(id=id)
            routes = navbar.get_formatted_routes(navbar.get_routes(
                request.user), active_page='vendor management')
            context = {}
            context.update({"routes": routes})
            context.update(
                {"title": "Details of {}".format(vendor.organizationName)})
            context.update({"sub_navbar": 'vendors'})

            # Orders and Delivery
            remaining_orders = order_models.Order.objects.filter( Q(vendor=vendor) and ~Q(status=3)).count()
            context.update({"remaining_orders": remaining_orders})

            delivered_orders = order_models.Order.delivered_objects.filter(vendor=vendor).count()
            context.update({"delivered_orders": delivered_orders})

            # Vendor User
            vendor_users = vendor.vendorUsers.all().count()
            context.update({"vendor_users": vendor_users})

            # Products, search, wishlist
            products = product_models.Product.objects.filter(vendor=vendor).count()
            context.update({"vendor_users": vendor_users})

            recent_added_products = product_models.Product.objects.filter(vendor=vendor).order_by('-created_at')[:4]
            context.update({"recent_added_products": recent_added_products})

            searched = analytics_views.highly_searched_keyword()
            highly_searched = product_models.Product.objects.filter(tags__in=[d for d in searched])
            context.update({"highly_searched": highly_searched})

            wishlist = cart_models.WishList.objects.filter(product__vendor=vendor)
            context.update({"wishlist": wishlist})

            # Groups
            groups = Group.objects.filter(vendor=vendor).count()
            context.update({"groups": groups})

            return render(request, template_version+"/Views/VendorView/details.html", context=context)
        except (Exception, vendor_models.VendorRequest.DoesNotExist) as e:
            print(e)
            messages.error(request, "Vendor does not exists.")
            return HttpResponseRedirect(reverse('vendor-vendors'))
