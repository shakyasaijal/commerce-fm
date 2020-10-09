from django.shortcuts import render
from django.conf import settings
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, action, api_view
import jwt

from Referral import models as refer_models
from Referral import serializers as refer_serializer
from Referral.utils import _generate_code


class JoinReferral(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = refer_models.Referral.objects.none()
    permission_classes = [IsAuthenticated]

    def create(self, request):
        try:
            refer_models.Referral.objects.get(user=request.user)
            return Response({"message": "You have participated."}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except (Exception, refer_models.Referral.DoesNotExist):
            code = _generate_code()
            new_refer_member = refer_models.Referral.objects.create(
                user=request.user, refer_code=code, refer_url=settings.FRONTEND_URL+code)
            return Response({"status": True, "data": {"code": new_refer_member.refer_code}}, status=status.HTTP_200_OK)
