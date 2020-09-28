from django.shortcuts import render, redirect, reverse
from django.conf import settings
from django.utils.decorators import method_decorator
from functools import wraps
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission


from DashboardManagement.common import routes as navbar
from Vendor import models as vendor_models
from User import models as user_models
from DashboardManagement.common import helper as app_helper
from DashboardManagement.validator import create as create_validation
from CartSystem import models as cart_models
from DashboardManagement.common import create as create_helper


template_version = "DashboardManagement/v1"
try:
    if settings.TEMPLATE_VERSION:
        template_version = "DashboardManagement/"+settings.TEMPLATE_VERSION
except Exception:
    pass


def vendor_only(function):
    @wraps(function)
    def _wrapped_view(request, *args, **kwargs):
        if settings.MULTI_VENDOR:
            vendors = vendor_models.Vendor.objects.all()
            if request.user.is_authenticated:
                for vendor in vendors:
                    if request.user in vendor.vendorUsers.all() or request.user == vendor.vendorAdmin:
                        return function(request, *args, **kwargs)
                messages.warning(request, 'Only vendors are allowed to login.')
                return render(request, template_version+"/Views/LoginView/login.html")
        else:
            if not request.user.is_superuser:
                messages.warning(request, 'Only vendors are allowed to login.')
                return render(request, template_version+"/Views/LoginView/login.html")
        return function(request, *args, **kwargs)
    return _wrapped_view


@method_decorator(vendor_only, name='dispatch')
class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        routes = navbar.get_formatted_routes(
            navbar.get_routes(request.user), active_page='dashboard')
        return render(request, template_version+"/index.html", context={'routes': routes, 'title': 'Dashboard'})


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('vendor-home'))
        return render(request, template_version+"/Views/LoginView/login.html")

    def post(self, request):
        try:
            user = authenticate(
                request, username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                login_user = False
                if settings.MULTI_VENDOR:
                    vendors = vendor_models.Vendor.objects.all()
                    for vendor in vendors:
                        if user in vendor.vendorUsers.all() or user == vendor.vendorAdmin:
                            login_user = True
                else:
                    if request.user.is_superuser:
                        login_user = True

                if login_user:
                    login(request, user)
                    messages.success(request, 'You are now logged in.')
                    return HttpResponseRedirect(reverse('vendor-home'))
                else:
                    if settings.MULTI_VENDOR:
                        messages.warning(
                            request, 'Only vendors are allowed to login.')
                    else:
                        messages.error(request, 'Access Denied.')
                return HttpResponseRedirect(reverse('vendor-login'))
            else:
                messages.warning(request, 'Invalid email/password.')
                return HttpResponseRedirect(reverse('vendor-login'))
        except (user_models.User.DoesNotExist, Exception) as e:
            print(e)
            messages.warning(request, 'Something went wrong. Please try again')
            return HttpResponseRedirect(reverse('vendor-login'))


class LogoutView(View):
    def post(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('vendor-login'))


# Groups and Permissions
@method_decorator(vendor_only, name='dispatch')
class GroupView(LoginRequiredMixin, View):
    def get(self, request):
        if not app_helper.access_management('auth.view_group', request):
            messages.error(
                request, "You do not have permission to group user data.")
            return HttpResponseRedirect(reverse('vendor-home'))

        context = {}
        context.update({'title': 'Groups and Permissions'})
        if settings.MULTI_VENDOR:
            all_groups = Group.objects.filter(
                vendor=app_helper.current_user_vendor(request.user))
        else:
            all_groups = Group.objects.all()
        context.update({'groups': all_groups})
        routes = navbar.get_formatted_routes(navbar.get_routes(
            request.user), active_page='groups and permissions')
        context.update({'routes': routes})
        return render(request, template_version+"/Views/GroupsAndPermissions/groups.html", context=context)


@method_decorator(vendor_only, name='dispatch')
class GroupDetailView(LoginRequiredMixin, View):
    def get(self, request, id):
        if not app_helper.access_management('auth.view_group', request):
            messages.error(
                request, "You do not have permission to view group data.")
            return HttpResponseRedirect(reverse('vendor-home'))

        context = {}
        all_perm = []
        group = Group.objects.get(id=id)
        if settings.MULTI_VENDOR:
            vendor = app_helper.current_user_vendor(request.user)
            if group.vendor != vendor:
                messages.error(request, "Group not found.")
                return HttpResponseRedirect(reverse('vendor-groups'))

        permissions = app_helper.permissions_of_group(group)
        all_permissions = Permission.objects.exclude(
            content_type_id__in=app_helper.excluding_permissions())

        for data in all_permissions:
            if data not in permissions:
                all_perm.append(data)

        context.update({"available_permissions": all_perm})
        context.update({"group": group})
        context.update({"permissions": permissions})
        routes = navbar.get_formatted_routes(navbar.get_routes(
            request.user), active_page='groups and permissions')
        context.update({'routes': routes})

        return render(request, template_version+"/Views/GroupsAndPermissions/groups-detail.html", context=context)

    def post(self, request, id):
        if not request.user.has_perm('auth.change_group') and not app_helper.is_vendor_admin(request.user):
            messages.error(
                request, "You do not have permission to change group data.")
            return HttpResponseRedirect(reverse('vendor-home'))

        try:
            grp = Group.objects.get(id=id)
            vendor = app_helper.current_user_vendor(request.user)
            if grp.vendor != vendor:
                messages.error(request, "Group not found.")
                return HttpResponseRedirect(reverse('vendor-groups'))
            grp.name = request.POST['name']
            grp.description = request.POST['description']
            grp.permissions.clear()
            for data in request.POST.getlist('to[]'):
                grp.permissions.add(Permission.objects.get(id=int(data)))
            grp.save()
            messages.success(request, "Modification success.")
            return redirect(request.META['HTTP_REFERER'])
        except Exception as e:
            print("Group modification: ", e)
            messages.error(
                request, "Modification Failed. Please try again later.")
            return HttpResponseRedirect(reverse('vendor-groups'))


@method_decorator(vendor_only, name='dispatch')
class CreateGroup(LoginRequiredMixin, View):
    def get_permissions(self):
        permissions = Permission.objects.exclude(
            content_type_id__in=app_helper.excluding_permissions())
        return permissions

    def get(self, request):
        if not app_helper.access_management('auth.add_group', request):
            messages.warning(
                request, "You do not have permission to add new group.")
            return HttpResponseRedirect(reverse('vendor-home'))

        context = {}
        context.update({"available_permissions": self.get_permissions()})
        routes = navbar.get_formatted_routes(navbar.get_routes(
            request.user), active_page='groups and permissions')
        context.update({'routes': routes})
        return render(request, template_version+"/Views/GroupsAndPermissions/create.html", context=context)

    def post(self, request):
        if not app_helper.access_management('auth.add_group', request):
            messages.error(
                request, "You do not have permission to add new group.")
            return HttpResponseRedirect(reverse('vendor-home'))

        new_group = Group.objects.none()
        validation = create_validation.create_group_validation(request)
        if not validation[0]:
            messages.error(request, "Error identified.")
            context = {}
            context.update({"error": validation[1]})
            try:
                context.update({"oldName": request.POST['name']})
                context.update({"oldDescription": request.POST['description']})
                context.update(
                    {"available_permissions": self.get_permissions()})
                routes = navbar.get_formatted_routes(navbar.get_routes(
                    request.user), active_page='groups and permissions')
                context.update({'routes': routes})
            except Exception as e:
                pass
            return render(request, template_version+"/Views/GroupsAndPermissions/create.html", context=context)
        try:
            if settings.MULTI_VENDOR:
                new_group = Group.objects.create(name=request.POST['name'], vendor=app_helper.current_user_vendor(
                    request.user), description=request.POST['description'])
            else:
                new_group = Group.objects.create(name=request.POST['name'], description=request.POST['description'])
            
            for data in request.POST.getlist('to[]'):
                new_group.permissions.add(Permission.objects.get(id=int(data)))

            messages.success(request, "Group successfully created.")
        except Exception as e:
            if new_group:
                new_group.delete()
            messages.error(
                request, "Failed to create new group. Please try again.")
        return HttpResponseRedirect(reverse('vendor-groups'))


@method_decorator(vendor_only, name='dispatch')
class DeleteGroup(LoginRequiredMixin, View):
    def get(self, request, id):
        return HttpResponseRedirect(reverse('vendor-groups'))

    def post(self, request, id):
        if not app_helper.access_management('auth.delete_group', request):
            messages.error(
                request, "You do not have permission to delete group.")
            return HttpResponseRedirect(reverse('vendor-home'))
        try:
            grp = Group.objects.get(id=id)

            if settings.MULTI_VENDOR:
                vendor = app_helper.current_user_vendor(request.user)
                if grp.vendor != vendor:
                    messages.error(request, "Group not found.")
                    return HttpResponseRedirect(reverse('vendor-groups'))
            grp.delete()
            messages.success(request, "Group successfully deleted.")
        except (Exception, Group.DoesNotExist) as e:
            print("Group deletion: ", e)
            messages.error(request, "Sorry. Unable to find the group.")
        return HttpResponseRedirect(reverse('vendor-groups'))


# Users
@method_decorator(vendor_only, name='dispatch')
class UsersView(LoginRequiredMixin, View):
    def get(self, request):
        if not app_helper.access_management('User.view_user', request):
            messages.error(
                request, "You do not have permission to view user data.")
            return HttpResponseRedirect(reverse('vendor-home'))
        context = {}
        routes = navbar.get_formatted_routes(
            navbar.get_routes(request.user), active_page='users')
        context.update({'routes': routes})
        context.update({'title': 'Users'})

        if settings.MULTI_VENDOR:
            vendor = app_helper.current_user_vendor(request.user)
            vendor_user = vendor.vendorUsers.all()
        else:
            vendor_user = user_models.User.objects.filter(is_superuser=True)
        context.update({'vendor_user': vendor_user})
        return render(request, template_version+"/Views/UserView/index.html", context=context)


@method_decorator(vendor_only, name='dispatch')
class CreateUser(LoginRequiredMixin, View):
    def common(self, request):
        routes = navbar.get_formatted_routes(
            navbar.get_routes(request.user), active_page='users')
        
        context = {}
        if settings.MULTI_VENDOR:
            all_groups = app_helper.get_all_groups_of_a_vendor(request.user)
        else:
            all_groups = Group.objects.all()

        districts = []
        locations = cart_models.Location.objects.all().order_by('district')
        for district in locations:
            districts.append(district)

        context.update({"routes": routes})
        context.update({"title": "Create User"})
        context.update({"all_groups": all_groups})
        context.update({'districts': districts})

        return context

    def get(self, request):
        if not app_helper.access_management('User.add_user', request):
            messages.error(
                request, "You do not have permission to add new user.")
            return HttpResponseRedirect(reverse('vendor-home'))
        context = self.common(request)
        return render(request, template_version+"/Views/UserView/add.html", context=context)

    def post(self, request):
        if not app_helper.access_management('User.add_user', request):
            messages.error(
                request, "You do not have permission to add new user.")
            return HttpResponseRedirect(reverse('vendor-home'))

        validation = create_validation.create_vendor_user_validation(
            request, from_='creation')
        context = self.common(request)
        if not validation[0]:
            messages.error(request, "Please fix the following errors.")
            context.update({'error': validation[1]})
            try:
                context.update({'old': request.POST})
            except Exception as e:
                pass
            return render(request, template_version+"/Views/UserView/add.html", context=context)
        else:
            create_vendor_user = create_helper.create_vendor_user(
                request, app_helper.current_user_vendor(request.user))
            if create_vendor_user:
                messages.success(request, "User successfully created.")
            else:
                try:
                    context.update({'old': request.POST})
                except Exception as e:
                    pass
                messages.error(
                    request, "Something went wrong. Please try again later.")
                return render(request, template_version+"/Views/UserView/add.html", context=context)
        return HttpResponseRedirect(reverse('vendor-users'))


@method_decorator(vendor_only, name='dispatch')
class DeleteUser(LoginRequiredMixin, View):
    def get(self, request, id):
        return HttpResponseRedirect(reverse('vendor-users'))

    def post(self, request, id):
        if not app_helper.access_management('User.delete_user', request):
            messages.error(
                request, "You do not have permission to delete user.")
            return HttpResponseRedirect(reverse('vendor-home'))

        try:
            user = user_models.User.objects.get(id=id)
            if settings.MULTI_VENDOR:
                vendor = app_helper.current_user_vendor(request.user)
                vendor_of_deletable_user = app_helper.vendor_of_a_user(user)
                if vendor_of_deletable_user != vendor:
                    messages.error(request, "User does not exists.")
                    return HttpResponseRedirect(reverse('vendor-users'))
            user.delete()
            messages.success(request, "User successfully deleted.")
        except (Exception, user_models.User.DoesNotExist) as e:
            print("User deletion: ", e)
            messages.error(request, "Sorry. Unable to find the user.")
        return HttpResponseRedirect(reverse('vendor-users'))


@method_decorator(vendor_only, name='dispatch')
class EditUser(LoginRequiredMixin, View):
    def common(self, request):
        context = {}
        routes = navbar.get_formatted_routes(
            navbar.get_routes(request.user), active_page='users')
        context.update({'routes': routes})
        context.update({'title': 'Edit User'})
        districts = []
        locations = cart_models.Location.objects.all().order_by('district')
        for district in locations:
            districts.append(district)

        context.update({'districts': districts})
        if settings.MULTI_VENDOR:
            all_group = app_helper.get_all_groups_of_a_vendor(request.user)
            context.update({'all_groups': all_group})
        return context

    def get(self, request, id):
        if not app_helper.access_management('User.view_user', request):
            messages.error(
                request, "You do not have permission to view user data.")
            return HttpResponseRedirect(reverse('vendor-home'))

        context = self.common(request)
        user = user_models.User.objects.none()
        try:
            user = user_models.User.objects.get(id=id)
        except (Exception, user_models.User.DoesNotExist) as e:
            messages.error(request, "User does not exists.")
            return HttpResponseRedirect(reverse('vendor-users'))
        context.update({'editUser': user})
        user_group = user.groups.all()
        context.update({"in_group": [grp.id for grp in user_group]})

        return render(request, template_version+"/Views/UserView/edit.html", context=context)

    def post(self, request, id):
        if not app_helper.access_management('User.change_user', request):
            messages.error(
                request, "You do not have permission to change user data.")
            return HttpResponseRedirect(reverse('vendor-home'))

        user = user_models.User.objects.none()
        try:
            user = user_models.User.objects.get(id=id)
            if settings.MULTI_VENDOR:
                current_user_vendor = app_helper.current_user_vendor(request.user)
                if user == current_user_vendor.vendorAdmin:
                    return HttpResponseRedirect(reverse('vendor-users'))
        except (Exception, user_models.User.DoesNotExist) as e:
            print(e)
            messages.error(request, "User does not exists.")
            return HttpResponseRedirect(reverse('vendor-users'))

        validations = create_validation.create_vendor_user_validation(
            request, from_='', id_=id)
        if not validations[0]:
            context = self.common(request)
            messages.error(request, "Something went wrong.")
            return redirect(request.META['HTTP_REFERER'])
        else:

            try:
                if request.POST['first_name']:
                    user.first_name = request.POST['first_name']
            except Exception:
                pass

            try:
                if request.POST['last_name']:
                    user.last_name = request.POST['last_name']
            except Exception:
                pass

            try:
                if settings.HAS_ADDITIONAL_USER_DATA:
                    if request.POST['district']:
                        user.user_profile.district = cart_models.Location.objects.get(
                            id=request.POST['district'])
            except (Exception, cart_models.Location.objects.none()):
                pass

            try:
                if settings.HAS_ADDITIONAL_USER_DATA:
                    if request.POST['address']:
                        user.user_profile.address = request.POST['address']
            except Exception:
                pass

            try:
                if settings.HAS_ADDITIONAL_USER_DATA:
                    if request.POST['phone']:
                        user.user_profile.phone = request.POST['phone'].strip()
            except Exception:
                pass

            try:
                if app_helper.access_management('auth.change_group', request):
                    user.groups.clear()
                    if request.POST.getlist('groups'):
                        # Add to Group
                        for data in request.POST.getlist('groups'):
                            Group.objects.get(id=data).user_set.add(user)
            except Exception as e:
                print(e)
                pass

            user.save()
            if settings.HAS_ADDITIONAL_USER_DATA:
                user.user_profile.save()
            messages.success(request, "User updated.")
            return redirect(request.META['HTTP_REFERER'])
