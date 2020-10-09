from django.conf import settings
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets, mixins, status

from CompanyInformation import models as company_info
from CompanyInformation import serializers as company_serializer


class CompanyInfo(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = company_info.CompanyInformation.objects.first()
    serializer_class = company_serializer.CompanySerializer
    permission_classes = [AllowAny]

    def list(self, request):
        company_data = self.get_queryset()
        social_media = company_serializer.SocialMediaSerializer(
            company_info.SocialMedia.objects.first())

        return Response({
            "companyInfo": {
                "name": settings.COMPANY_NAME,
                "email": company_data.email,
                "phone": [{
                    "number": d.number,
                    "of": d.of
                }for d in company_data.phone.all()],
                "address": company_data.address,
                "fax": company_data.fax,
                "postBox": company_data.post_box
            },
            "socialMedia": social_media.data
        }, status=status.HTTP_200_OK)
