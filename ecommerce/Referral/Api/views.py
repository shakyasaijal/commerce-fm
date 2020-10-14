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
            responseData = {
                "referCode": referUser.refer_code,
                "referUrl": referUser.refer_url
            }
        except (Exception, refer_models.Referral.DoesNotExist):
            # Referal Activation
            code = utils._generate_code(generateFor='user')

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

            responseData = {
                "referCode": code,
                "referUrl": refer_url,
                "data": data
            }
        return Response({"status": True, "data": {"code": responseData}}, status=status.HTTP_200_OK)


class ProcessReferral(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = refer_models.Referral.objects.none()
    permission_classes = [AllowAny]

    def create(self, request):
        try:
            refer_code = request.data['refer_code']
            split_refer_code = refer_code.split(':')
            process_of = split_refer_code[0]
            code = split_refer_code[1]
        except (Exception, IndexError):
            return Response({"status": False, "data": {"msg": "Something went wrong. Please try again."}}, status=status.HTTP_404_NOT_FOUND)

        # Common
        agent_data = utils.user_agent_data(request)
        agent_data.update({"ip": utils.get_ip(request)})

        if process_of == "urk":
            try:
                key = utils.generate_refered_user_key(agent_data, "user")
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
        elif process_of == "vrk":
            try:
                key = utils.generate_refered_user_key(agent_data, "vendor")
                vendorRefer_instance = refer_models.VendorKey.objects.get(
                    key=key)
                return Response({"status": False, "data": {"msg": "You have already been referred by {}".format(vendorRefer_instance.referredFrom.vendor.organizationName)}}, status=status.HTTP_406_NOT_ACCEPTABLE)
            except (Exception, refer_models.VendorKey.DoesNotExist) as e:
                print(e)
            try:
                vendor_refer = refer_models.VendorReferral.objects.get(
                    refer_code=code)
                vendor_reward = refer_models.VendorReward.objects.get(
                    referral=vendor_refer)
                vendor_reward.visited = vendor_reward.visited+1
                vendor_reward.save()
                refer_models.VendorKey.objects.get_or_create(
                    key=key, referredFrom=vendor_refer)
                return Response({"status": True, "data": {"__uik": key, "referredBy": vendor_refer.vendor.organizationName}}, status=status.HTTP_201_CREATED)
            except (Exception, refer_models.VendorReferral.DoesNotExist, refer_models.VendorReward.DoesNotExist) as e:
                print(e)
                return Response({"status": False, "data": {"msg": "Refer code invalid."}}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"status": False, "data": {"msg": "Refer code invalid."}}, status=status.HTTP_404_NOT_FOUND)


class Analytics(viewsets.ModelViewSet):
    queryset = refer_models.Referral.objects.none()
    permission_classes = [IsAuthenticated]

    def list(self, request):
        try:
            user_referal = refer_models.Referral.objects.get(user=request.user)
            data = {
                "referCode": user_referal.refer_code,
                "referUrl": user_referal.refer_url
            }
            user_reward = refer_models.Reward.objects.get(
                referral=user_referal)
            data.update({
                "points": user_reward.points,
                "visited": user_reward.visited,
                "signedUp": user_reward.signed_up,
                "buyed": user_reward.buyed
            })
            user_block = refer_models.Block.objects.get(user=request.user)
            descendant = utils.childBlocks(user_block)
            data.update({"descendantMade": descendant})
            return Response({"data": data}, status=status.HTTP_200_OK)
        except (Exception, refer_models.Referral.DoesNotExist, refer_models.Reward.DoesNotExist):
            return Response({"status": False, "data": {"msg": "You have not activated refer account."}}, status=status.HTTP_404_NOT_FOUND)
