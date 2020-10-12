

from DashboardManagement.common import helper as app_helper
from Referral import models as refer_models


def vendor_refer_analysis(vendor):
    data = {}

    try:
        vendor_refer = refer_models.VendorReferral.objects.get(vendor=vendor)
        refer_reward = refer_models.VendorReward.objects.get(referral=vendor_refer)

        data.update({
            "referCode": vendor_refer.refer_code,
            "referUrl": vendor_refer.refer_url,
            "referReward": refer_reward
        })
    except (Exception, refer_models.VendorReferral.DoesNotExist):
        pass

    try:
        block = refer_models.VendorBlock.objects.get(vendor=vendor)
        descendant_blocks = app_helper.childBlocks(block)
        data.update({"childBlock": descendant_blocks})
    except (Exception, refer_models.Block.DoesNotExist) as e:
        print(e)
        pass

    return data
