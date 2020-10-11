from django.shortcuts import render, redirect
from django.conf import settings
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, action, api_view
import jwt

import datetime

from Referral import models as refer_models
from Referral import serializers as refer_serializer
from Referral import utils


class JoinReferral(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = refer_models.Referral.objects.none()
    permission_classes = [IsAuthenticated]

    def create(self, request):
        try:
            referUser = refer_models.Referral.objects.get(user=request.user)
            data = {
                "referCode": referUser.refer_code,
                "referUrl": referUser.refer_url
            }
        except (Exception, refer_models.Referral.DoesNotExist):
            # Referal Activation
            code = utils._generate_code()

            refer_url = settings.FRONTEND_REFER_URL+"{}:".format("urk")+code
            new_refer_member = refer_models.Referral.objects.create(
                user=request.user, refer_code=code, refer_url=refer_url)

            # Default Reward Object
            refer_models.Reward.objects.create(referral=new_refer_member)

            # Block Chain for tracking
            '''
            Since new referal activation is a genesis block.
            Genesis: True
            Previous Hash: Null or default value
            '''
            data = {
                "userId": request.user.id,
                "email": request.user.email,
                "timestamp": datetime.datetime.timestamp(datetime.datetime.now())
            }
            genesis = True
            data_hash = utils.hash_data(str(data))
            refer_models.Block.objects.create(
                data=str(data), data_hash=data_hash, genesis_block=genesis, user=request.user)

            response = {
                "referCode": code,
                "referUrl": refer_url,
                "data": data
            }
        return Response({"status": True, "data": {"code": response}}, status=status.HTTP_200_OK)


class ProcessReferral(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = refer_models.Referral.objects.none()
    permission_classes = [AllowAny]

    def create(self, request):
        refer_code = request.data['refer_code']
        split_refer_code = refer_code.split(':')
        code = split_refer_code[1]
        agent_data = utils.user_agent_data(request)
        agent_data.update({"ip": utils.get_ip(request)})
        key = utils.generate_refered_user_key(agent_data)

        try:
            refer_instance = refer_models.UserKey.objects.get(key=key)
            return Response({"status": False, "data": {"msg": "You have already been referred by {}".format(refer_instance.referredFrom.user.get_full_name())}}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except (Exception, refer_models.UserKey.DoesNotExist):
            pass

        try:
            refer = refer_models.Referral.objects.get(refer_code=code)
            reward = refer_models.Reward.objects.get(referral=refer)
            reward.visited = reward.visited + 1
            reward.save()
            refer_models.UserKey.objects.get_or_create(
                key=key, referredFrom=refer)
            return Response({"status": True, "data": {"__uik": key, "referredBy": refer.user.get_full_name()}}, status=status.HTTP_201_CREATED)
        except (Exception, refer_models.Referral.DoesNotExist, refer_models.Reward.DoesNotExist) as e:
            print(e)
            return Response({"status": False, "data": {"msg": "Refer code invalid."}}, status=status.HTTP_404_NOT_FOUND)
