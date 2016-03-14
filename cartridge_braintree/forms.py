from __future__ import unicode_literals

import json

from django import forms
from django.utils.html import format_html
from django.forms.utils import flatatt
from django.utils.translation import ugettext as _

from cartridge.shop.forms import OrderForm
from cartridge.shop import checkout

from cartridge_braintree.utils import get_country_list


class NoNameTextInput(forms.TextInput):
    """ A widget for a text input that omits the 'name' attribute, which
    should prevent them from being submitted to the server.
    """

    def render(self, name, value, attrs=None):
        # See django.forms.widgets.py,
        # class Input, method render()
        if attrs is None:
            attrs = {}
        attrs['autocomplete'] = 'off'
        # Triggers number keyboard on iPhone. Using together with
        # 'novalidate' attribute for checkout form, which prevents
        # html5 validation errors for spaces.
        attrs['pattern'] = '[0-9]*'
        attrs['inputmode'] = 'numeric'
        final_attrs = self.build_attrs(attrs, type=self.input_type)
        # Remove the name from the attributes, as this is what this
        # widget is for!
        if 'name' in final_attrs:
            final_attrs.pop('name')
        # Never add the value to the HTML rendering, this field
        # will be encrypted and should remain blank if the form is
        # re-loaded!
        final_attrs['value'] = ''
        return format_html('<input{0} />', flatatt(final_attrs))


class BraintreeOrderForm(OrderForm):
    """
    The following change are made to the cartridge order form:
    - Shipping and Billing country fields are rendered using
      a Select widget. This ensures the country selected can be
      converted to a valid code for Braintree's payment processing.
    - Credit Card number and CCV fields are rendered using the
      NoNameTextInput widget so that the data is not submitted to the server.
      Javascript processes these fields to create a payment_method_nonce,
      which is then stored in a hidden form element.
    - Using jquery.payment from stripe for client-side validation of the payment
      form and submit the errors in the hidden braintree_errors field to the server
      to handle them as Django errors.

      See https://developers.braintreepayments.com/guides/transactions/python
    """

    payment_method = forms.CharField(label=_("Payment Method"), required=False)
    payment_method_nonce = forms.CharField(label=_("Payment Method Nonce"), required=False)
    braintree_errors = forms.CharField(label=_("Braintree Errors"), required=False)

    def __init__(self, request, step, data=None, initial=None, errors=None):
        super(BraintreeOrderForm, self).__init__(request, step, data, initial, errors)
        self.fields["payment_method"].widget = forms.HiddenInput()
        self.fields["payment_method"].value = "card"
        self.fields["payment_method_nonce"].widget = forms.HiddenInput()
        self.fields["payment_method_nonce"].value = ""
        self.fields["braintree_errors"].widget = forms.HiddenInput()
        self.fields["braintree_errors"].value = ""

        # Get list of tuples with country alpha2 codes and translated country names
        country_list = get_country_list()

        # Change country widgets to a Select widget
        if not isinstance(self.fields["billing_detail_country"].widget, forms.HiddenInput):
            # Billing country field is not hidden
            self.fields["billing_detail_country"].widget = forms.Select(choices=country_list)
        if not isinstance(self.fields["shipping_detail_country"].widget, forms.HiddenInput):
            # Shipping country field is not hidden
            self.fields["shipping_detail_country"].widget = forms.Select(choices=country_list)

        # The card number and CCV fields should have the 'name' attribute removed
        # and the fields made non-required, as they will be handled by the javascript
        # and remain blank when hitting the server.
        if not isinstance(self.fields["card_number"].widget, forms.HiddenInput):
            # Card number is not hidden
            attrs = {
                'placeholder': '0000 0000 0000 0000',            }
            self.fields["card_number"].widget = NoNameTextInput(attrs=attrs)
            self.fields["card_number"].required = False
        if not isinstance(self.fields["card_ccv"].widget, forms.HiddenInput):
            # Card CCV is not hidden
            attrs = {
                'placeholder': '000',
            }
            self.fields["card_ccv"].widget = NoNameTextInput(attrs=attrs)
            self.fields["card_ccv"].required = False

    def clean(self):
        """
        See if the payment form returned any errors
        See if the payment_method_nonce was created successfully.
        """
        if self.cleaned_data["step"] >= checkout.CHECKOUT_STEP_PAYMENT:
            if self.cleaned_data["payment_method"] == "card":
                braintree_errors = self.cleaned_data["braintree_errors"]
                if braintree_errors:
                    errors = json.loads(braintree_errors)
                    if 'cardName' in errors and errors['cardName'] == 'blank':
                        self._errors["card_name"] = self.error_class([_("This field is required.")])
                    if 'cardNumber' in errors and errors['cardNumber'] == 'blank':
                        self._errors["card_number"] = self.error_class([_("This field is required.")])
                    elif 'cardNumber' in errors and errors['cardNumber'] == 'invalid':
                        self._errors["card_number"] = self.error_class([_("A valid card number is required.")])
                    if 'cardExpiry' in errors and errors['cardExpiry'] == 'invalid':
                        self._errors["card_expiry_year"] = self.error_class([_("A valid expiry date is required.")])
                    if 'cardCCV' in errors and errors['cardCCV'] == 'blank':
                        self._errors["card_ccv"] = self.error_class([_("This field is required.")])
                    elif 'cardCCV' in errors and errors['cardCCV'] == 'invalid':
                        self._errors["card_ccv"] = self.error_class([_("A valid CCV is required.")])
                    if 'cardType' in errors and errors['cardType'] == 'blank':
                        self._errors["card_type"] = self.error_class([_("This field is required.")])
                    elif 'cardType' in errors and errors['cardType'] == 'invalid':
                        self._errors["card_type"] = self.error_class([_("The card type selected doesn't match your card number.")])
                    if 'tokenizeCard' in errors and errors['tokenizeCard'] == 'failed':
                        raise forms.ValidationError(_("Credit Card Number/CCV could not be processed. Please try again."))
                elif not self.cleaned_data["payment_method_nonce"]:
                    # Payment Method Nonce is blank, but braintree_errors is also blank - this may occur
                    # if e.g. javascript is disabled
                    # Although we have warnings in place (see braintreejs.html and payment.html)
                    # We should catch this here rather than later.
                    raise forms.ValidationError(_("Credit Card Number/CCV could not be processed. Please try again."))

            else:
                # PayPal Payment
                # Remove blank card_name and card_type from errors
                self.errors.pop("card_name", None)
                self.errors.pop("card_type", None)

        return super(BraintreeOrderForm, self).clean()
