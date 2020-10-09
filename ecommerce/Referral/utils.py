import random
from Referral import models as refer_models


def _generate_code():
    def generate_code():
        t = "abcdefghijkmnopqrstuvwwxyzABCDEFGHIJKLOMNOPQRSTUVWXYZ1234567890"
        return "".join([random.choice(t) for i in range(40)])
    code = generate_code()
    while refer_models.Referral.objects.filter(refer_code=code).exists():
        code = _generate_code()
    return code
