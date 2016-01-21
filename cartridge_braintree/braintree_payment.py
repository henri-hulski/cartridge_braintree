from __future__ import unicode_literals
from future.builtins import str
from django.core.exceptions import ImproperlyConfigured
from mezzanine.conf import settings

from cartridge.shop.checkout import CheckoutError

# Requires Braintree package -- install from pypi: pip install braintree.
try:
    import braintree
except ImportError:
    raise ImproperlyConfigured("Braintree package must be installed.")


if settings.DEBUG:
    BRAINTREE_ENVIROMENT = braintree.Environment.Sandbox
else:
    BRAINTREE_ENVIROMENT = braintree.Environment.Production

try:
    BRAINTREE_MERCHANT_ID = settings.BRAINTREE_MERCHANT_ID
    BRAINTREE_PUBLIC_KEY = settings.BRAINTREE_PUBLIC_KEY
    BRAINTREE_PRIVATE_KEY = settings.BRAINTREE_PRIVATE_KEY
except AttributeError:
    raise ImproperlyConfigured("You need to define BRAINTREE_MERCHANT_ID, "
                               "BRAINTREE_PUBLIC_KEY and BRAINTREE_PRIVATE_KEY "
                               "in your settings module to use the "
                               "Braintree v.zero payment processor.")


BRAINTREE_IS_CONFIGURED = False


def configure():
    global BRAINTREE_IS_CONFIGURED
    braintree.Configuration.configure(
        BRAINTREE_ENVIROMENT,
        BRAINTREE_MERCHANT_ID,
        BRAINTREE_PUBLIC_KEY,
        BRAINTREE_PRIVATE_KEY
    )
    BRAINTREE_IS_CONFIGURED = True


def client_token():
    # verify that braintree has been configured, if not, call configure()
    if not BRAINTREE_IS_CONFIGURED:
        configure()

    return braintree.ClientToken.generate()


def payment_handler(request, order_form, order):
    """
    Braintree payment handler.

    See https://www.braintreepayments.com/docs/python/transactions/create

    Raise cartride.shop.checkout.CheckoutError("error message") if
    payment is unsuccessful.

    In your settings, set ``SHOP_HANDLER_PAYMENT`` to point to this function,
    'cartridge_braintree.braintree_payment.payment_handler'

    """
    # verify that braintree has been configured, if not, call configure()
    if not BRAINTREE_IS_CONFIGURED:
        configure()

    data = order_form.cleaned_data

    trans = {
        'payment_method_nonce': data['payment_method_nonce'],
        'amount': order.total,
        'order_id': str(order.id),
        'customer': {
            'first_name': data['billing_detail_first_name'],
            'last_name': data['billing_detail_last_name'],
            'email': data['billing_detail_email'],
            'phone': data['billing_detail_phone'],
        },
        'billing': {
            'first_name': data['billing_detail_first_name'],
            'last_name': data['billing_detail_last_name'],
            'street_address': data['billing_detail_street'],
            'locality': data['billing_detail_city'],
            'region': data['billing_detail_state'],
            'postal_code': data['billing_detail_postcode'],
            'country_code_alpha2': data['billing_detail_country'],
        },
        'shipping': {
            'first_name': data['shipping_detail_first_name'],
            'last_name': data['shipping_detail_last_name'],
            'street_address': data['shipping_detail_street'],
            'locality': data['shipping_detail_city'],
            'region': data['shipping_detail_state'],
            'postal_code': data['shipping_detail_postcode'],
            'country_code_alpha2': data['shipping_detail_country'],
        },
        'options': {
            'submit_for_settlement': True
        }
    }

    # Send transaction to braintree
    result = braintree.Transaction.sale(trans)
    if result.is_success:
        return result.transaction.id
    else:
        raise CheckoutError("Credit Card error: " + result.message)
