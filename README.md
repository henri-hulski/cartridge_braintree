cartridge_braintree
===================

Braintree Payments processing for Mezzanine/Cartridge

********************************************************************************************
NOTE: This fork is no longer maintained as of January 2016 
Please instead use https://github.com/henri-hulski/cartridge_braintree as the main reference.
********************************************************************************************

Note that this is very much a first pass and has not been thoroughly tested. 

I have no intention of formally publishing this as a full PyPI package, but I'm happy for someone to take this initial code and expand it into a full package.

Instructions for use
--------------------

1. Install cartridge_braintree
    pip install git+https://github.com/molokov/cartridge_braintree.git

2. Add cartridge_braintree to your INSTALLED_APPS. List it higher than
'cartridge.shop', otherwise the cartridge_braintree template will not
be selected.

3. Set up the following settings in your settings.py/local_settings.py

    BRAINTREE_ENV - "Sandbox" or "Production"
    BRAINTREE_MERCHANT - your merchant ID
    BRAINTREE_PUBLIC_KEY - your public key
    BRAINTREE_PRIVATE_KEY - your private key
    BRAINTREE_CLIENT_SIDE_ENCRYPTION_KEY - your client side encryption key for braintree.js

See also https://support.braintreepayments.com/customer/portal/articles/1080475-api-keys

4. Set the order form to be the modified Braintree form (in settings.py)
   
    SHOP_CHECKOUT_FORM_CLASS = 'cartridge_braintree.forms.BraintreeOrderForm'

This form does the following:
- Changes the shipping and billing country fields to a Select widget
  This ensures that the country selected can be converted to a valid
  code for Braintree's payment processing.
  The default selected country can be selected by settings.SHOP_DEFAULT_COUNTRY
  which is also editable in the admin.
- Changes Credit Card number and CVV to custom widgets that will generate
  data encrypted form inputs as required by braintree.js
  Note also CCV becomes a password input rather than just text.

5. Set the payment handler to be the Braintree payment handler

    SHOP_HANDLER_PAYMENT = 'cartridge_braintree.braintree_payment.payment_handler'
   
The templates provided with this package ensure that the credit card fields are encrypted on the client side using braintree.js. If you are overriding the templates in your own apps, then be sure to include the relevant braintreejs.html template.

See https://www.braintreepayments.com/docs/python/guide/getting_paid for Braintree's tutorial.   

