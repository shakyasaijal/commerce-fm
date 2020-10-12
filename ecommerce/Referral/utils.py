import random
import uuid
import hashlib
from Referral import models as refer_models
from user_agents import parse


def _generate_code(generateFor='user'):
    def generate_code():
        t = "abcdefghijkmnopqrstuvwwxyzABCDEFGHIJKLOMNOPQRSTUVWXYZ1234567890"
        return "".join([random.choice(t) for i in range(40)])
    code = generate_code()
    if generateFor == 'user':
        while refer_models.Referral.objects.filter(refer_code=code).exists():
            code = generate_code()
    else:
        while refer_models.VendorReferral.objects.filter(refer_code=code).exists():
            code = generate_code()
    return code

def ensure_session_key(request):
    """
    Given a request return a session key that will be used. There may already
    be a session key associated, but if there is not, we force the session to
    create itself and persist between requests for the client behind the given
    request.
    """
    key = request.session.session_key
    if key is None:
        # @@@ Django forces us to handle session key collision amongst
        # multiple processes (not handled)
        request.session.save()
        # force session to persist for client
        request.session.modified = True
        key = request.session.session_key
    return key


def hash_data(data):
    # uuid is used to generate a random number
    return hashlib.sha256(data.encode()).hexdigest()


def generate_refered_user_key(data, key_of="user"):
    uik = hash_data(str(data))
    if key_of == "user":
        uik = "urk:"+uik
    else:
        uik = "vrk:"+uik
    return uik


def get_ip(request):
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    except Exception:
        return None


def get_user_agent(request):
    try:
        return request.META['HTTP_USER_AGENT']
    except Exception:
        return None


def user_agent_data(request):
    agent_data = get_user_agent(request)
    parse_agent = parse(agent_data)
    data = {
        "osFamily": parse_agent.os.family,
        "osVersion": parse_agent.os.version_string or "",
        "deviceFamily": parse_agent.device.family,
        "deviceBrand": parse_agent.device.brand or ""
    }
    return data
