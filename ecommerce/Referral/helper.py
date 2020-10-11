import datetime
from django.conf import settings

from Referral import models as refer_models
from Referral import utils


def join_refer_by_vendor(vendor):
    try:
        referUser = refer_models.VendorReferral.objects.get(vendor=vendor)
        return False, "Referal Feature has already been activated."
    except (Exception, refer_models.Referral.DoesNotExist):
        # Referal Activation
        code = utils._generate_code(generateFor='vendor')
        refer_url = settings.FRONTEND_REFER_URL+"{}:".format("vrk")+code
        new_refer_member = refer_models.VendorReferral.objects.create(
            vendor=vendor, refer_code=code, refer_url=refer_url)

        # Default Reward Object
        refer_models.VendorReward.objects.create(referral=new_refer_member)

        # Block Chain for tracking
        '''
        Since new referal activation is a genesis block.
        Genesis: True
        Previous Hash: Null or default value
        '''
        data = {
            "vendorId": vendor.id,
            "name": vendor.organizationName,
            "timestamp": datetime.datetime.timestamp(datetime.datetime.now())
        }
        genesis = True
        data_hash = utils.hash_data(str(data))
        refer_models.VendorBlock.objects.create(
            data=str(data), data_hash=data_hash, genesis_block=genesis, vendor=vendor)

        return True, "You have successfully activated Referal Feature."
    return False, "Something went wrong. Please try again."
