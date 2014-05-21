#!/usr/bin/env python

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html
from django.forms.util import flatatt
from django.utils.encoding import force_text

from mezzanine.conf import settings
from cartridge.shop.forms import OrderForm
from cartridge.shop import checkout
from cartridge.shop.utils import make_choices

from cartridge_braintree.countries import get_country_names_list

class DataEncryptedTextInput(forms.TextInput):
    def render(self, name, value, attrs=None):
        # See django.forms.widgets.py,
        # class Input, method render()
        if value is None:
            value = ''
        if attrs is None:
            attrs = {}
        attrs['name'] = name
        attrs['autocomplete'] = 'off'
        attrs['data-encrypted-name'] = name           
        final_attrs = self.build_attrs(attrs, type=self.input_type)
        # Never add the value to the HTML rendering, this field 
        # will be encrypted and should remain blank if the form is
        # re-loaded!
        final_attrs['value'] = ''
        return format_html('<input{0} />', flatatt(final_attrs))

class DataEncryptedPasswordInput(DataEncryptedTextInput):
    input_type = 'password'

class BraintreeOrderForm(OrderForm):
    """
    The following changes are made to the cartridge order form:
    - Shipping and Billing country fields are rendered using
      a Select widget. This ensures the country selected can be
      converted to a valid code for Braintree's payment processing.
    - Credit Card number and CCV fields are rendered using the
      DataEncryptedTextInput and DataEncryptedPasswordInput widgets
      so that the HTML form inputs match what is required for braintree.js     

      See https://www.braintreepayments.com/docs/python/guide/getting_paid 
    """

    def __init__(self, request, step, data=None, initial=None, errors=None):
        OrderForm.__init__(self, request, step, data, initial, errors)

        is_first_step = step == checkout.CHECKOUT_STEP_FIRST
        is_last_step = step == checkout.CHECKOUT_STEP_LAST
        is_payment_step = step == checkout.CHECKOUT_STEP_PAYMENT

        # Get list of country names
        countries = make_choices(get_country_names_list())
    
        if settings.SHOP_CHECKOUT_STEPS_SPLIT:
            if is_first_step:
                # Change country widgets to a Select widget
                self.fields["billing_detail_country"].widget = forms.Select(choices=countries)
                self.fields["billing_detail_country"].initial = settings.SHOP_DEFAULT_COUNTRY
                self.fields["shipping_detail_country"].widget = forms.Select(choices=countries)
                self.fields["shipping_detail_country"].initial= settings.SHOP_DEFAULT_COUNTRY
            if is_payment_step:
                # Make card number and cvv fields use the data encrypted widget
                self.fields["card_number"].widget = DataEncryptedTextInput()
                self.fields["card_ccv"].widget = DataEncryptedPasswordInput()
        else:
            # Change country widgets to a Select widget
            self.fields["billing_detail_country"].widget = forms.Select(choices=countries)
            self.fields["billing_detail_country"].initial = settings.SHOP_DEFAULT_COUNTRY            
            self.fields["shipping_detail_country"].widget = forms.Select(choices=countries)
            self.fields["shipping_detail_country"].initial= settings.SHOP_DEFAULT_COUNTRY
            if settings.SHOP_PAYMENT_STEP_ENABLED:
                # Make card number and cvv fields use the data encrypted widget
                self.fields["card_number"].widget = DataEncryptedTextInput()
                self.fields["card_ccv"].widget = DataEncryptedPasswordInput()

