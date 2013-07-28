from django.core.exceptions import ImproperlyConfigured
from mezzanine.conf import settings

import braintree
from cartridge.shop.checkout import CheckoutError
from cartridge_braintree.countries import get_country_code_alpha2

try:
    BRAINTREE_ENV = settings.BRAINTREE_ENV
    BRAINTREE_MERCHANT = settings.BRAINTREE_MERCHANT
    BRAINTREE_PUBLIC_KEY = settings.BRAINTREE_PUBLIC_KEY
    BRAINTREE_PRIVATE_KEY = settings.BRAINTREE_PRIVATE_KEY
    BRAINTREE_CLIENT_SIDE_ENCRYPTION_KEY = settings.BRAINTREE_CLIENT_SIDE_ENCRYPTION_KEY
    # The Client side encryption key setting is defined in defaults.py but it still needs
    # to be set to a non-blank value
    if BRAINTREE_CLIENT_SIDE_ENCRYPTION_KEY == "":
        raise AttributeError()    
except AttributeError:
    raise ImproperlyConfigured("You need to define BRAINTREE_ENV, BRAINTREE_MERCHANT, "
                               "BRAINTREE_PUBLIC_KEY, BRAINTREE_PRIVATE_KEY, and "
                               "BRAINTREE_CLIENT_SIDE_ENCRYPTION_KEY "
                               "in your settings module to use the "
                               "braintree payment processor.")

IS_CONFIGURED = False
def configure():   
    envs = { 'Sandbox' : braintree.Environment.Sandbox,
             'Production' : braintree.Environment.Production }

    try:
        env = envs[BRAINTREE_ENV]
    except KeyError:
        raise ImproperlyConfigured("BRAINTREE_ENV '{0}' is not valid. Must be one of {1}".
                format(BRAINTREE_ENV, sorted(envs.keys())))

    braintree.Configuration.configure(env,
        BRAINTREE_MERCHANT,
        BRAINTREE_PUBLIC_KEY,
        BRAINTREE_PRIVATE_KEY
        )
    IS_CONFIGURED = True


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
    if not IS_CONFIGURED:
        configure()

    trans = {}
    amount = order.total
    trans['amount'] = amount

    trans['order_id'] = str(order.id)

    data = order_form.cleaned_data
    trans['customer'] = {
        'first_name': data['billing_detail_first_name'],
        'last_name': data['billing_detail_last_name'],
        'email': data['billing_detail_email'],
        'phone': data['billing_detail_phone'],
    }
    trans['billing'] = {
        'first_name': data['billing_detail_first_name'],
        'last_name': data['billing_detail_last_name'],
        'street_address': data['billing_detail_street'],
        'locality': data['billing_detail_city'],
        'region': data['billing_detail_state'],
        'postal_code': data['billing_detail_postcode'],
        'country_code_alpha2': get_country_code_alpha2(data['billing_detail_country']),
    }
    trans['shipping'] = {
        'first_name': data['shipping_detail_first_name'],
        'last_name' : data['shipping_detail_last_name'],
        'street_address': data['shipping_detail_street'],
        'locality': data['shipping_detail_city'],
        'region': data['shipping_detail_state'],
        'postal_code': data['shipping_detail_postcode'],
        'country_code_alpha2': get_country_code_alpha2(data['shipping_detail_country']),
    }
    trans['credit_card'] = {
        'cardholder_name' : data['card_name'],
        'number': data['card_number'].replace(' ', ''),
        'expiration_month': data['card_expiry_month'],
        'expiration_year': data['card_expiry_year'],
        'cvv': data['card_ccv'],
    }
    trans ['options'] = { "submit_for_settlement" : True }

    # Send transaction to braintree
    result = braintree.Transaction.sale(trans)
    if result.is_success:
        return result.transaction.id
    else:
        raise CheckoutError(result.message)


