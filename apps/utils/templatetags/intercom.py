from django import template
from django.conf import settings

import hmac, hashlib

register = template.Library()

@register.filter
def intercom_sha_256(user_id):
    return hmac.new(settings.INTERCOM_SECRET_KEY, str(user_id), digestmod=hashlib.sha256).hexdigest()
