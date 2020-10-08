from django.conf import settings
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site

from User import models as user_models
from User import serializers as user_serializers
from DashboardManagement.common import emails as send_email


class RegisterUser(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    queryset = user_models.User.objects.all()
    serializer_class = user_serializers.UserRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = user_serializers.UserRegisterSerializer(data=request.data)

        if serializer.is_valid():
            email_data = {
                "current_site": get_current_site(request).domain,
                "secure": request.is_secure() and "https" or "http",
                "email": request.data["email"],
                "full_name": request.data["first_name"]+" "+request.data['last_name'],
                "from": None,
            }
            if settings.CELERY_FOR_EMAIL:
                sendEmail = send_email.send_email_with_delay.delay(
                    "Registration Verification", email_data)
            else:
                sendEmail = send_email.send_email_without_delay(
                    "Registration Verification", email_data)

            if not sendEmail:
                return Response({"status": False, "data": {"message": "User not registered. There was problem sending verification email."}}, status=400)

            serializer.save()
            user = user_models.User.objects.none()
            try:
                user = user_models.User.objects.get(
                    email=request.data["email"])
                refresh_token = user.refresh_token
                user.refresh_tokens = refresh_token
                user.save()
                data = {
                    "userId": user.id,
                    "email": user.email,
                    "isVerified": user.is_verified,
                    "accessToken": user.access_token,
                    "refreshToken": refresh_token
                }
                return Response({"status": True, "data": data}, status=200)
            except (user_models.User.DoesNotExist):
                if user:
                    user.delete()
                return Response({"status": False, "data": {"message": "User not registered. Please try again."}}, status=400)
        else:
            return Response({"status": False, "data": {"message": "User not registered. Please try again.", "errors": serializer.errors}}, status=401)
