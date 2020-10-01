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
from django.db.models import Q, Sum, Count
from rest_framework.response import Response
from rest_framework.decorators import api_view

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
            context.update({"vendor": vendor})
            context.update(
                {"title": "Details of {}".format(vendor.organizationName)})
            context.update({"sub_navbar": 'vendors'})

            # Orders and Delivery
            '''
               remaining_orders         : Remaining orders of a vendor
               remaining_orders_of_all  : Remaining orders of all vendors
               r_percentage_covered       : Total Percentage Covered by a vendor in total orders
            '''
            remaining_orders = order_models.Order.objects.filter( Q(vendor=vendor) & ~Q(status=3))
            context.update({"remaining_orders": remaining_orders.count()})
            remaining_orders_of_all = order_models.Order.objects.filter( ~Q(status=3)).count()
            context.update({"remaining_orders_of_all": remaining_orders_of_all})
            r_percentage_covered = round((remaining_orders.count()/remaining_orders_of_all)*100, 2)
            context.update({"r_percentage_covered": r_percentage_covered})

            '''
               delivered_orders         : Delivered orders of a vendor
               delivered_orders_of_all  : Delivered orders of all vendors
               percentage_covered       : Total Percentage Covered by a vendor in total orders
            '''
            delivered_orders = order_models.Order.delivered_objects.filter(vendor=vendor)
            context.update({"delivered_orders": delivered_orders.count()})
            delivered_orders_of_all = order_models.Order.delivered_objects.filter().count()
            context.update({"delivered_orders_of_all": delivered_orders_of_all})
            d_percentage_covered = round((delivered_orders.count()/delivered_orders_of_all)*100, 2)
            context.update({"d_percentage_covered": d_percentage_covered})

            # Vendor User
            '''
               vendor_users             : Users of a vendor
               all_vendor_user          : Users of all vendors
               vu_percentage_covered    : Total Percentage Covered by a vendor in total orders
            '''
            vendor_users = vendor.vendorUsers.all().count()
            context.update({"vendor_users": vendor_users})
            all_vendor_user = vendor_models.Vendor.objects.aggregate(total=Count('vendorUsers'))['total']
            context.update({"all_vendor_user": all_vendor_user})
            vu_percentage_covered = round((vendor_users/all_vendor_user)*100, 2)
            context.update({"vu_percentage_covered": vu_percentage_covered})


            
            # Products, search, wishlist
            '''
               products                : Products of a vendor
               all_products            : Products of all vendors
               p_percentage_covered    : Total Percentage Covered by a vendor in products
            '''
            products = product_models.Product.objects.filter(vendor=vendor).count()
            context.update({"products": products})
            all_products = product_models.Product.objects.all().count()
            context.update({"all_products": all_products})
            p_percentage_covered = round((products/all_products)*100, 2)
            context.update({"p_percentage_covered": p_percentage_covered})

            recent_added_products = product_models.Product.objects.filter(vendor=vendor).order_by('-created_at')[:5]
            context.update({"recent_added_products": recent_added_products})

            searched = analytics_views.highly_searched_keyword()
            tags = product_models.Tags.objects.filter(tag__in=[d for d in searched])
            highly_searched = product_models.Product.objects.filter(tags__in=tags, vendor=vendor).distinct()[:8]
            context.update({"highly_searched": highly_searched})

            wishlist = cart_models.WishList.objects.filter(product__vendor=vendor)
            context.update({"wishlist": wishlist})

            # Most Expensive and Least Expensive Products
            least_expensive = product_models.Product.objects.filter(vendor=vendor).order_by('price')[:1]
            if least_expensive:
                context.update({"least_expensive_product": least_expensive[0]})
                least_expensive_sold = order_models.OrderItem.objects.filter(item=least_expensive[0]).aggregate(total=Sum('quantity'))
                context.update({"least_expensive_product_sold": least_expensive_sold['total']})

            most_expensive = product_models.Product.objects.filter(vendor=vendor).order_by('-price')[:1]
            if most_expensive:
                context.update({"most_expensive_product": most_expensive[0]})
                most_expensive_sold = order_models.OrderItem.objects.filter(item=most_expensive[0]).aggregate(total=Sum('quantity'))
                context.update({"most_expensive_product_sold": most_expensive_sold['total']})
                
            total_quantity_sold = order_models.OrderItem.objects.aggregate(Sum('quantity'))
            context.update({"total_quantity_sold": total_quantity_sold['quantity__sum']})

            # Groups
            '''
               groups                  : Groups of a vendor
               all_groups              : Groups of all vendors
               g_percentage_covered    : Total Percentage Covered by a vendor in total groups
            '''
            groups = Group.objects.filter(vendor=vendor).count()
            context.update({"groups": groups})
            all_groups = Group.objects.count()
            context.update({"all_groups": all_groups})
            g_percentage_covered = round((groups/all_groups)*100, 2)
            context.update({"g_percentage_covered": g_percentage_covered})

            # print(request.headers['Referer'])
            return render(request, template_version+"/Views/VendorView/details.html", context=context)
        except (Exception, vendor_models.VendorRequest.DoesNotExist) as e:
            print(e)
            messages.error(request, "Vendor does not exists.")
            return HttpResponseRedirect(reverse('vendor-vendors'))


@api_view(['GET'])
def TopFiveCategory(request):
    try:
        vendor = vendor_models.Vendor.objects.get(id=request.data['vendorId'])
    except (Exception, vendor_models.Vendor.DoesNotExist):
        pass
    data = analytics_views.top_five_category()
    return Ressponse(data, status=200)
