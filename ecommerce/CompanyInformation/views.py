from django.shortcuts import render
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.conf import settings
from django.views import View
from django.db.models import Q

from DashboardManagement.views import vendor_only
from DashboardManagement.common import helper as app_helper
from DashboardManagement.common import routes as navbar
from CompanyInformation import models as company_models
from CompanyInformation import forms as company_forms


template_version = "CompanyInformation/v1"
try:
    if settings.TEMPLATE_VERSION:
        template_version = "CompanyInformation/"+settings.TEMPLATE_VERSION
except Exception:
    pass


@method_decorator(vendor_only, name='dispatch')
class CompanyInformation(LoginRequiredMixin, View):
    def get(self, request):
        if not app_helper.access_management('CompanyInformation.view_companyinformation', request):
            messages.error(
                request, "You do not have permission to view company information.")
            return HttpResponseRedirect(reverse('vendor-home'))
        context = {}
        routes = navbar.get_formatted_routes(navbar.get_routes(
            request.user), active_page='company information')
        context.update({"routes": routes})
        context.update({"title": "Company Information"})
        info = company_models.CompanyInformation.objects.first()
        info_forms = company_forms.CompanyInfoForm(instance=info)

        social_media = company_models.SocialMedia.objects.first()
        social_forms = company_forms.SocialMediaForm(instance=social_media)

        contacts = company_models.ContactNumber.objects.all()
        contact_form = company_forms.ContactForm()

        context.update({"infoForms": info_forms, "socialForms": social_forms,
                        "contacts": contacts, "contactForm": contact_form})
        return render(request, template_version+"/view.html", context=context)


@method_decorator(vendor_only, name='dispatch')
class CreateContact(LoginRequiredMixin, View):
    def post(self, request):
        if not app_helper.access_management('CompanyInformation.add_contactnumber', request):
            messages.error(
                request, "You do not have permission to add new contact number.")
            return HttpResponseRedirect(reverse('vendor-home'))

        form = company_forms.ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Contact Created.")
            return HttpResponseRedirect(reverse('vendor-company-info'))
        else:
            context = {}
            routes = navbar.get_formatted_routes(navbar.get_routes(
                request.user), active_page='company information')
            context.update({"routes": routes})
            context.update({"title": "Company Information"})
            info = company_models.CompanyInformation.objects.first()
            info_forms = company_forms.CompanyInfoForm(instance=info)

            social_media = company_models.SocialMedia.objects.first()
            social_forms = company_forms.SocialMediaForm(instance=social_media)
            contacts = company_models.ContactNumber.objects.all()

            context.update({"infoForms": info_forms, "socialForms": social_forms,
                            "contacts": contacts, "contactForm": form})
            return render(request, template_version+"/view.html", context=context)


@method_decorator(vendor_only, name='dispatch')
class DeleteContact(LoginRequiredMixin, View):
    def post(self, request, id):
        if not app_helper.access_management('CompanyInformation.delete_contactnumber', request):
            messages.error(
                request, "You do not have permission to delete contact number.")
            return HttpResponseRedirect(reverse('vendor-home'))

        try:
            company_models.ContactNumber.objects.get(id=id).delete()
            messages.success(request, "Contact sucessfully deleted.")
        except (Exception, company_models.ContactNumber.DoesNotExist):
            messages.warning(request, "Contact not found.")
        return HttpResponseRedirect(reverse('vendor-company-info'))


@method_decorator(vendor_only, name='dispatch')
class EditContact(LoginRequiredMixin, View):
    def post(self, request, id):
        if not app_helper.access_management('CompanyInformation.change_contactnumber', request):
            messages.error(
                request, "You do not have permission to edit contact number.")
            return HttpResponseRedirect(reverse('vendor-home'))

        try:
            haveData = company_models.ContactNumber.objects.filter(
                ~Q(id=id) & Q(number=request.POST['phone{}'.format(id)]))
            if haveData:
                messages.warning(request, "Contact number must be unique.")
            else:
                data = company_models.ContactNumber.objects.get(id=id)
                data.number = request.POST['phone{}'.format(id)]
                data.of = request.POST['name{}'.format(id)]
                data.save()
                messages.success(request, "Contact updated successfully.")
            return HttpResponseRedirect(reverse('vendor-company-info'))
        except (Exception, company_models.ContactNumber.DoesNotExist) as e:
            print(e)
            messages.warning(request, "Contact not found.")
        return HttpResponseRedirect(reverse('vendor-company-info'))


@method_decorator(vendor_only, name='dispatch')
class EditInfo(LoginRequiredMixin, View):
    def post(self, request):
        if not app_helper.access_management('CompanyInformation.add_companyinformation', request):
            messages.error(
                request, "You do not have permission to add contact number.")
            return HttpResponseRedirect(reverse('vendor-home'))

        if not app_helper.access_management('CompanyInformation.change_companyinformation', request):
            messages.error(
                request, "You do not have permission to edit contact number.")
            return HttpResponseRedirect(reverse('vendor-home'))

        info = company_models.CompanyInformation.objects.first()
        if info:
            form = company_forms.CompanyInfoForm(request.POST, instance=info)
            if form.is_valid:
                form.save()
                messages.success(request, "Basic information updated.")
            else:
                messages.error(
                    request, "Something went wrong. Please try again later.")
        else:
            form = company_forms.CompanyInfoForm(request.POST)
            if form.is_valid:
                form.save()
                messages.success(request, "Basic information updated.")
            else:
                messages.error(
                    request, "Something went wrong. Please try again later.")
        return HttpResponseRedirect(reverse('vendor-company-info'))


@method_decorator(vendor_only, name='dispatch')
class EditSocialInfo(LoginRequiredMixin, View):
    def post(self, request):
        if not app_helper.access_management('CompanyInformation.add_socialmedia', request):
            messages.error(
                request, "You do not have permission to add social links.")
            return HttpResponseRedirect(reverse('vendor-home'))

        if not app_helper.access_management('CompanyInformation.change_socialmedia', request):
            messages.error(
                request, "You do not have permission to edit social links.")
            return HttpResponseRedirect(reverse('vendor-home'))

        info = company_models.SocialMedia.objects.first()
        if info:
            form = company_forms.SocialMediaForm(request.POST, instance=info)
            if form.is_valid:
                form.save()
                messages.success(request, "Social Links Updated.")
            else:
                messages.error(
                    request, "Something went wrong. Please try again later.")
        else:
            form = company_forms.SocialMediaForm(request.POST)
            if form.is_valid:
                form.save()
                messages.success(request, "Social Links Updated.")
            else:
                messages.error(
                    request, "Something went wrong. Please try again later.")
        return HttpResponseRedirect(reverse('vendor-company-info'))
