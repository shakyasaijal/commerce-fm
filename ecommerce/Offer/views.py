from django.shortcuts import render, redirect, reverse
from django.conf import settings
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from DashboardManagement.common import routes as navbar
from DashboardManagement.common import helper as app_helper
from DashboardManagement.views import vendor_only
from Offer import models as offer_models
from . import forms as offer_forms
from Products import models as product_models


template_version = "Offer/v1"
try:
    if settings.TEMPLATE_VERSION:
        template_version = "Offer/"+settings.TEMPLATE_VERSION
except Exception:
    pass

@method_decorator(vendor_only, name='dispatch')
class OfferView(LoginRequiredMixin, View):
    def get(self, request):
        if not app_helper.access_management('Offer.view_offer', request):
            messages.error(
                request, "You do not have permission to change products.")
            return HttpResponseRedirect(reverse('vendor-home'))

        if settings.MULTI_VENDOR:
            if not request.user.is_superuser:
                offers = offer_models.Offer.objects.filter(vendor=app_helper.current_user_vendor(request.user))
            else:
                offers = offer_models.Offer.objects.all()
        else:
            offers = offer_models.Offer.objects.all()

        routes = navbar.get_formatted_routes(navbar.get_routes(
            request.user), active_page='special offers')
        context = {}
        context.update({"routes": routes})
        context.update({"offers": offers})
        context.update({"title": "Special Offers"})
        context.update({"sub_navbar": "all offers"})

        return render(request, template_version+"/view.html", context=context)


@method_decorator(vendor_only, name='dispatch')
class AddOfferView(LoginRequiredMixin, View):
    def common(self, request):
        context = {}
        routes = navbar.get_formatted_routes(navbar.get_routes(
            request.user), active_page='special offers')
        context.update({"title": "Add Special Offers"})
        context.update({"routes": routes})
        return context

    def get(self, request):
        if (not request.user.is_superuser):
            messages.error(
                request, "You do not have permission to add offers.")
            return HttpResponseRedirect(reverse('vendor-home'))

        context = {}
        context.update(self.common(request))
        context.update({"form": offer_forms.OfferForm()})
        return render(request, template_version+"/add.html", context=context)

    def post(self, request):
        if (not request.user.is_superuser):
            messages.error(
                request, "You do not have permission to add offers.")
            return HttpResponseRedirect(reverse('vendor-home'))

        form = offer_forms.OfferForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "New Offer successfully created.")
            return HttpResponseRedirect(reverse('vendor-offers'))
        else:
            context = {}
            context.update({"routes": self.common(request)})
            context.update({"form": form})
            messages.error(request, "Please correct the following errors.")
            return render(request, template_version+"/add.html", context=context)


class DeleteOffers(LoginRequiredMixin, View):
    def post(self, request):
        if (not request.user.is_superuser):
            messages.error(
                request, "You do not have permission to add offers.")
            return HttpResponseRedirect(reverse('vendor-home'))

        try:
            offer = offer_models.Offer.objects.get(id=request.POST['id'])
            offer.delete()
            messages.success(request, "Special Offer successfully deleted.")
            return HttpResponseRedirect(reverse('vendor-offers'))
        except (Exception, offer_models.Offer.DoesNotExist):
            messages.error(request, "No such offer found.")
            return HttpResponseRedirect(reverse('vendor-offers'))


class EditOffers(LoginRequiredMixin, View):
    def common(self, request, title):
        context = {}
        routes = navbar.get_formatted_routes(navbar.get_routes(
            request.user), active_page='special offers')
        context.update({"title": "Edit {}".format(title)})
        context.update({"routes": routes})
        return context

    def get(self, request, id):
        if (not request.user.is_superuser):
            messages.error(
                request, "You do not have permission to add offers.")
            return HttpResponseRedirect(reverse('vendor-home'))
        context = {}

        try:
            offer = offer_models.Offer.objects.get(id=id)
            form = offer_forms.OfferForm(instance=offer)
            context.update({"form": form})
            context.update(self.common(request, offer.title))
            return render(request, template_version+"/edit.html", context=context)
        except (Exception, offer_models.Offer.DoesNotExist):
            messages.error(request, "No such offer found.")
            return HttpResponseRedirect(reverse('vendor-offers'))

    def post(self, request, id):
        if (not request.user.is_superuser):
            messages.error(
                request, "You do not have permission to add offers.")
            return HttpResponseRedirect(reverse('vendor-home'))
        context = {}

        try:
            offer = offer_models.Offer.objects.get(id=id)
            form = offer_forms.OfferForm(request.POST, request.FILES, instance=offer)
            if form.is_valid():
                form.save()
                messages.success(request, "Special Offer successfully deleted.")
                return HttpResponseRedirect(reverse('vendor-offers'))
            context.update({"form": form})
            context.update(self.common(request, offer.title))
            return render(request, template_version+"/edit.html", context=context)
        except (Exception, offer_models.Offer.DoesNotExist):
            messages.error(request, "No such offer found.")
            return HttpResponseRedirect(reverse('vendor-offers'))


class ListProductToAddInOffer(LoginRequiredMixin, View):
    def get(self, request, id):
        if (not app_helper.access_management('Product.add_product', request)
                and not app_helper.is_vendor_admin(request.user)):
            messages.error(
                request,
                "You do not have permission to add products to offers."
            )
            return HttpResponseRedirect(reverse('vendor-home'))
        context = {
            'title': 'Add Product To Offer'
        }
        offer = offer_models.Offer.objects.get(id=id)
        if settings.MULTI_VENDOR and not request.user.is_superuser:
            products = product_models.Product.objects.filter(
                vendor=app_helper.current_user_vendor(request.user),
                offers=None)\
                .order_by("-id")
        else:
            products = product_models.Product.objects.all().order_by("-id")
        routes = navbar.get_formatted_routes(navbar.get_routes(
            request.user), active_page='products')
        discounts = offer.discounts.split(',')
        context['routes'] = routes
        context['offer'] = offer
        context['products'] = products
        context['discounts'] = discounts
        return render(
            request,
            template_version+"/productList.html",
            context=context
        )

    def post(self, request, id):
        if not app_helper.access_management('Products.change_product', request):
            messages.error(
                request, "You do not have permission to change products.")
            return HttpResponseRedirect(reverse('vendor-home'))

        try:
            offer = offer_models.Offer.objects.get(id=id)
            product = product_models.Product.objects.get(id=request.POST['product_id'])
        except (product_models.Product.DoesNotExist,
                offer_models.Offer.DoesNotExits):
            messages.warning(
                request, 'There seems to be something wrong')
            return HttpResponseRedirect(reverse('products'))
        print(request.POST.getlist('offer_category'), "sssssssssssssssssssss")
        for i in request.POST.getlist('offer_category'):
            product.offer_category.add(
                offer_models.OfferCategory.objects.get(id=int(i)))
        product.discount = request.POST['discount']
        product.offers = offer
        product.save()
        messages.success(request, "Product added in Offer successfully.")
        return HttpResponseRedirect(
            reverse('add-product-to-offer', kwargs={'id': id}))
