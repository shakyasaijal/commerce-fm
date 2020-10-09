from django.conf import settings
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, logout
import jwt
import requests
import json
from rest_framework_simplejwt.tokens import RefreshToken

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

            serializer.save()
            user = user_models.User.objects.none()
            try:
                user = user_models.User.objects.get(
                    email=request.data["email"])
                token = RefreshToken.for_user(user)
                data = {
                    "email": user.email,
                    "isVerified": user.is_verified,
                    "accessToken": str(token.access_token),
                    "refreshToken": str(token)
                }
                return Response({"status": True, "data": data}, status=status.HTTP_200_OK)
            except (user_models.User.DoesNotExist):
                if user:
                    user.delete()
                return Response({"status": False, "data": {"message": "User not registered. Please try again."}}, status=status.HTTP_409_CONFLICT)
        else:
            return Response({"status": False, "data": {"message": "User not registered. Please try again.", "errors": serializer.errors}}, status=status.HTTP_406_NOT_ACCEPTABLE)


class LoginUser(mixins.CreateModelMixin,
                viewsets.GenericViewSet):
    serializer_class = user_serializers.LoginSerializer
    permission_classes = [AllowAny]

    @csrf_exempt
    def create(self, request):
        serializer = user_serializers.LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = request.data["email"]
            password = request.data["password"]
            try:
                check = user_models.User.objects.get(email=email)
                user = authenticate(
                    request, username=request.data["email"], password=request.data["password"])
            except (user_models.User.DoesNotExist, Exception):
                return Response({"status": False, "data": {"message": "Invalid credentials"}}, status=status.HTTP_404_NOT_FOUND)
            if user:
                token = RefreshToken.for_user(user)
                data = {
                    "userId": user.id,
                    "email": user.email,
                    "isVerified": user.is_verified,
                    "accessToken": str(token.access_token),
                    "refreshToken": str(token)
                }
                return Response({"status": True, "data": data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": False, "data": {"message": "Invalid credentials"}}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response({"status": False, "data": {"message": "Invalid credentials", "error": serializer.errors}}, status=status.HTTP_406_NOT_ACCEPTABLE)


class LogoutUser(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = user_serializers.LogoutSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"logout": True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Refresh Token is required"}, status=status.HTTP_404_NOT_FOUND)


class GoogleLogin(mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = user_serializers.GoogleLoginSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        id_token = request.data['idToken']
        url = "https://www.googleapis.com/oauth2/v3/tokeninfo?id_token=" + id_token
        response = requests.get(url)
        info = json.loads(response.text)
        if 'error_description' in info:
            return Response({"status": False, "data": {"message": info}}, status=status.HTTP_404_NOT_FOUND)
        email = info['email']
        try:
            user = user_models.User.objects.get(email=email)
            token = RefreshToken.for_user(user)
            data = {
                'userId': user.id,
                'email': user.email,
                'isVerified': user.is_verified,
                'accessToken': str(token.access_token),
                'refreshToken': str(token),
            }
            if not user.google_id:
                user.google_id = info['sub']
                user.is_verified = True
                user.save()
            return Response({"status": True, "data": data}, status=status.HTTP_200_OK)
        except (Exception, user_models.User.DoesNotExist) as e:
            data = {
                'first_name': info['given_name'],
                'last_name': info['family_name'],
                'email': email,
                'username': email
            }
            try:
                user = user_models.User.objects.create(**data)
                user.is_verified = True
                user.google_id = info['sub']
                token = RefreshToken.for_user(user)
                res = {
                    "userId": user.id,
                    "email": user.email,
                    "isVerified": user.is_verified,
                    "accessToken": str(token.access_token),
                    "refreshToken": str(token)
                }
                return Response({"status": True, "data": res}, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return Response({"status": False, "data": {"message": 'Could not login with google.Please Try again'}}, status=status.HTTP_409_CONFLICT)


class FacebookLogin(mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = user_serializers.FacebookLoginSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        access_token = request.data['accessToken']
        url = "https://graph.facebook.com/v3.3/me?fields=id,first_name,last_name,email&access_token=" + access_token
        response = requests.get(url)
        info = json.loads(response.text)
        if 'error' in info:
            return Response({"status": False, "data": {"message": info}}, status=status.HTTP_404_NOT_FOUND)
        email = info['email']
        try:
            user = user_models.User.objects.get(email=email)
            token = RefreshToken.for_user(user)
            data = {
                'userId': user.id,
                'email': user.email,
                'isVerified': user.is_verified,
                'accessToken': str(token.access_token),
                'refreshToken': str(token),
            }
            if not user.facebook_id:
                user.facebook_id = info['id']
                user.is_verified = True
                user.save()
            return Response({"status": True, "data": data}, status=status.HTTP_200_OK)
        except (Exception, user_models.User.DoesNotExist) as e:
            data = {
                'first_name': info['first_name'],
                'last_name': info['last_name'],
                'email': email,
                'username': email
            }
            try:
                user = user_models.User.objects.create(**data)
                user.is_verified = True
                user.facebook_id = info['id']
                token = RefreshToken.for_user(user)
                res = {
                    "userId": user.id,
                    "email": user.email,
                    "isVerified": user.is_verified,
                    "accessToken": str(token.access_token),
                    "refreshToken": str(token)
                }
                return Response({"status": True, "data": res}, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return Response({"status": False, "data": {"message": 'Could not login with facebook.Please Try again'}}, status=status.HTTP_409_CONFLICT)
