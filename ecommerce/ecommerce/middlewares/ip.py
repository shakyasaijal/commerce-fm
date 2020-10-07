from django.conf import settings
from django.contrib.gis.geoip2 import GeoIP2
from User import models as user_models


class IpAddress:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        try:
            geo = GeoIP2()
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            try:
                new_city = user_models.CityFromIpAddress.objects.get_or_create(city=geo.city(ip))
                new_ip = user_models.IpAddress.objects.get_or_create(ip=ip, city=new_city)
            except Exception:
                new_ip = user_models.IpAddress.objects.get_or_create(ip=ip)

            if new_ip:
                request.new_ip = new_ip[0]
            else:
                request.new_ip = None
            
            if settings.HAS_ADDITIONAL_USER_DATA:
                if request.user.is_authenticated and new_ip:
                    try:
                        user_profile = user_models.UserProfile.objects.get(user=request.user)
                        user_profile.ip.add(new_ip[0])
                        user_profile.save()
                    except (Exception, user_models.UserProfile.DoesNotExist) as e:
                        print("Ip Middleware: ", e)
                        pass
        except Exception:
            pass    