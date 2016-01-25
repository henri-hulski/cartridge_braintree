from __future__ import unicode_literals

from django.conf.urls import url
from mezzanine.conf import settings

from cartridge.shop import views

from cartridge_braintree import braintree_payment


extra_context = {"client_token": braintree_payment.client_token()}

_slash = "/" if settings.APPEND_SLASH else ""

urlpatterns = [
    url("^%s$" % _slash, views.checkout_steps, {'extra_context': extra_context}, name="shop_checkout"),
]
