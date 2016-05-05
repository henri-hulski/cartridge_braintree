from __future__ import unicode_literals

from django.conf.urls import url

from mezzanine.conf import settings
from cartridge.shop import views

from cartridge_braintree import braintree_payment, forms


_slash = "/" if settings.APPEND_SLASH else ""

extra_context = {"client_token": braintree_payment.client_token()}
extra_options = {
    'form_class': forms.BraintreeOrderForm,
    'extra_context': extra_context,
}

urlpatterns = [
    url("^checkout%s$" % _slash,
        views.checkout_steps,
        extra_options,
        name="shop_checkout"),
]
