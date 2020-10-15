from django.shortcuts import render, redirect, reverse
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.utils.decorators import method_decorator
from functools import wraps
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout


from DeliverySystem import models as delivery_models

# Create your views here.
template_version = "DeliverySystem/v1"
try:
    if settings.TEMPLATE_VERSION:
        template_version = "DeliverySystem/"+settings.TEMPLATE_VERSION
except Exception:
    pass


def deliveryPerson_only(function):
    @wraps(function)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please login.')
            return HttpResponseRedirect(reverse('delivery-login'))
        if request.user.is_superuser:
            return function(request, *args, **kwargs)
        else:
            try:
                delivery_person = delivery_models.DeliveryPerson.objects.get(
                    user=request.user)
                print(delivery_person)
                return function(request, *args, **kwargs)
            except (Exception, delivery_models.DeliveryPerson.DoesNotExist):
                messages.warning(request, 'Access to delivery person only.')
                return render(request, template_version+"/Views/LoginView/login.html")
        return function(request, *args, **kwargs)
    return _wrapped_view


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('delivery-index'))
        return render(request, template_version+"/Views/LoginView/login.html")

    def post(self, request):
        

        user = authenticate(
                request, username=request.POST['email'], password=request.POST['password'])
        
        if user is not None:
            try:
                delivery_person = delivery_models.DeliveryPerson.objects.get(user=user)
                login(request, user)
                return HttpResponseRedirect(reverse('delivery-index'))
            except (Exception, delivery_models.DeliveryPerson.DoesNotExist):
                return redirect(settings.FRONTEND_URL)    
        else:
            messages.warning(request, 'Invalid email/password.')
            return HttpResponseRedirect(reverse('delivery-login'))



@method_decorator(deliveryPerson_only, name='dispatch')
class Index(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, template_version+"/Views/index.html")
