from __future__ import unicode_literals

from django.conf.urls import patterns, url

from cartridge_braintree import braintree_payment


extra_context = {"client_token": braintree_payment.client_token()}

urlpatterns = patterns("cartridge.shop.views",
    url('^$', "checkout_steps", {'extra_context': extra_context}, name="shop_checkout"),
)
