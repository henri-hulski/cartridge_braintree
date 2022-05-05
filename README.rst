cartridge_braintree
===================

Braintree Payments processing for Mezzanine/Cartridge.
Supports Django 3.2 or 4.0, Mezzanine 5.1 or newer and
Cartridge 1.3 or newer.

Instructions for use
--------------------

1. Install cartridge_braintree::

      pip install cartridge_braintree


   If you need the correct sorting of not ASCII country names use::

      pip install cartridge_braintree[countries_utf8_sorting]


   This will add 'pyuca' to the requirements.

2. Add 'cartridge_braintree' to your ``INSTALLED_APPS``. List it higher than
   'cartridge.shop', otherwise the cartridge_braintree template will
   not be selected.

3. Set up the following settings in your ``settings.py`` or ``local_settings.py``::

      BRAINTREE_MERCHANT_ID = <your merchant ID>
      BRAINTREE_PUBLIC_KEY = <your public key>
      BRAINTREE_PRIVATE_KEY = <your private key>

   .. Note::
      When ``DEBUG`` is ``True`` the *Braintree Sandbox environment* will be
      used, otherwise the *Braintree Production environment* is used.

   See also
   https://developer.paypal.com/braintree/articles/control-panel/important-gateway-credentials

4. cartridge_braintree uses a modified checkout form, which does the following:

   - Changes the shipping and billing country fields to a Select
     widget. This ensures that the country selected can be converted to
     a valid code for Braintree's payment processing.
     The supported countries can be set in ``settings.SHOP_SUPPORTED_COUNTRIES``,
     which is a list of alpha2 country codes and/or tuples in the form
     (alpha2, country_name).

     For example if you want to select the countries in the EU area use::

        SHOP_SUPPORTED_COUNTRIES = [
            'AL', 'AT', 'BA', 'BE', 'BG', 'CH', 'CY', 'DE', 'DK', 'EE', 'ES',
            'FI', 'FR', 'GB', 'GR', 'HR', 'HU', 'IE', 'IS', 'IT', 'LT', 'LV',
            'MK', 'MT', 'NL', 'NO', 'PL', 'PT', 'RO', 'RS', 'SE', 'SI'
         ]

     A pre-selected country in the select field can be specified using
     ``settings.SHOP_DEFAULT_COUNTRY`` as an alpha2 code.
     By default the user is expected to choose their country (set to ``None``).

     The country/countries (as alpha2 codes) listed in
     ``settings.SHOP_PRIMARY_COUNTRIES`` will show up at the top of the
     country selection fields, after the ``settings.SHOP_DEFAULT_COUNTRY``
     if set.

   - Credit Card number and CCV fields are rendered using the
     ``NoNameTextInput`` widget so that the data is not submitted to the
     server. Javascript processes these fields to create a
     ``payment_method_nonce``, which is then stored in a hidden form
     element.

   - Uses `jquery.payment <https://github.com/stripe-archive/jquery.payment>`_ from stripe
     for client-side validation of the payment form and submits the errors in the
     hidden ``braintree_errors`` field to the server to handle them as Django errors.

   See
   https://developer.paypal.com/braintree/docs/guides/transactions/python

5. Set the payment handler to be the Braintree payment handler::

      SHOP_HANDLER_PAYMENT = 'cartridge_braintree.braintree_payment.payment_handler'

   If you are overriding the templates in your own apps, then be sure to
   include the relevant ``braintreejs.html`` template.

6. Include ``cartridge_braintree.urls`` for ``shop/checkout`` in ``urls.py``
   before Cartridge urls::

      urlpatterns += [

          # cartridge_braintree URLs.
          re_path(r"^shop/(?=checkout(/?)$)", include("cartridge_braintree.urls")),

          # Cartridge URLs.
          path("shop/", include("cartridge.shop.urls")),
          path("account/orders/", order_history, name="shop_order_history"),

7. If you want to use PayPal payments with Braintree activate them in
   the Admin Site Settings and set the currency to use with PayPal.

   Alternatively you can set them in ``settings.py`` in the form::

      BRAINTREE_PAYPAL_ACTIVATE = True
      BRAINTREE_PAYPAL_CURRENCY = "EUR"

   In this case the settings will not be shown in the Admin.

8. Optionally add logging to your Django configuration if you want to have more details
   on transactions::

     LOGGING = {
         'version': 1,
         'disable_existing_loggers': False,
         'handlers': {
             'braintree_file': {
                 'class': 'logging.FileHandler',
                 'filename': '/path/to/django/braintree.log',
             },
         },
         'loggers': {
             'braintree_payment': {
                 'handlers': ['braintree_file'],
                 'level': 'DEBUG',
             },
         },
     }

   See https://docs.djangoproject.com/en/4.0/topics/logging/#configuring-logging for all
   configuration options

   Log levels are as follows:
    - Client token creation: info
    - Transaction start: debug
    - Transaction complete: debug
    - Transaction fail: warning

   Confidential information is never output to the logger.
