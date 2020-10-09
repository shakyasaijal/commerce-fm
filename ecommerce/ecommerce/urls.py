from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from security.views import csp_report

from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('', include('frontend.urls')),
    path('v1/api/', include('Api.urls')),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('dashboard/', include('DashboardManagement.urls')),
    path("csp-report/", csp_report),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

admin.site.site_header = settings.COMPANY_NAME
