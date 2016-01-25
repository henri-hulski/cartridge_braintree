from __future__ import unicode_literals

from django.conf.urls import url

from cartridge.shop import views

from cartridge_braintree import braintree_payment, forms


extra_context = {"client_token": braintree_payment.client_token()}
extra_options = {
    'form_class': forms.BraintreeOrderForm,
    'extra_context': extra_context,
}

urlpatterns = [
    url("^$", views.checkout_steps, extra_options, name="shop_checkout"),
]
