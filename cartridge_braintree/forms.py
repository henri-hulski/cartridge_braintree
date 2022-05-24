import json

from cartridge.shop import checkout
from cartridge.shop.forms import OrderForm
from django import forms
from django.forms.utils import flatatt
from django.utils.html import format_html
from django.utils.translation import gettext as _

from cartridge_braintree.utils import get_country_list


class NoNameTextInput(forms.TextInput):
    """A widget for a text input that omits the 'name' attribute, which
    should prevent them from being submitted to the server.
    """

    def render(self, name, value, attrs=None, renderer=None):
        # See django.forms.widgets.py,
        # class Input, method render()
        if attrs is None:
            attrs = {}
        attrs["autocomplete"] = "off"
        # Triggers number keyboard on iPhone. Using together with
        # 'novalidate' attribute for checkout form, which prevents
        # html5 validation errors for spaces.
        attrs["pattern"] = "[0-9]*"
        attrs["inputmode"] = "numeric"
        final_attrs = self.build_attrs(attrs, {"type": self.input_type})
        # Remove the name from the attributes, as this is what this
        # widget is for!
        if "name" in final_attrs:
            final_attrs.pop("name")
        # Never add the value to the HTML rendering, this field
        # will be encrypted and should remain blank if the form is
        # re-loaded!
        final_attrs["value"] = ""
        return format_html("<input{0}>", flatatt(final_attrs))


class BraintreeOrderForm(OrderForm):
    """
    The following change are made to the cartridge order form:
    - Remove card_name and card_type fields.
    - Make state/region fields optional.
    - Rearrange field order.
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

    card_name = None
    card_type = None

    field_order = [
        "billing_detail_first_name",
        "billing_detail_last_name",
        "billing_detail_street",
        "billing_detail_postcode",
        "billing_detail_city",
        "billing_detail_state",
        "billing_detail_country",
        "billing_detail_phone",
        "billing_detail_email",
        "shipping_detail_first_name",
        "shipping_detail_last_name",
        "shipping_detail_street",
        "shipping_detail_postcode",
        "shipping_detail_city",
        "shipping_detail_state",
        "shipping_detail_country",
        "shipping_detail_phone",
        "additional_instructions",
        "discount_code",
    ]

    payment_method = forms.CharField(label=_("Payment Method"), required=False)
    payment_method_nonce = forms.CharField(
        label=_("Payment Method Nonce"), required=False
    )
    braintree_errors = forms.CharField(label=_("Braintree Errors"), required=False)

    def __init__(self, request, step, data=None, initial=None, errors=None):
        super().__init__(request, step, data, initial, errors)
        self.fields["payment_method"].widget = forms.HiddenInput()
        self.fields["payment_method"].value = "card"
        self.fields["payment_method_nonce"].widget = forms.HiddenInput()
        self.fields["payment_method_nonce"].value = ""
        self.fields["braintree_errors"].widget = forms.HiddenInput()
        self.fields["braintree_errors"].value = ""

        # Get list of tuples with country alpha2 codes and translated country names
        country_list = get_country_list()

        # Change country widgets to a Select widget
        if not isinstance(
            self.fields["billing_detail_country"].widget, forms.HiddenInput
        ):
            # Billing country field is not hidden
            self.fields["billing_detail_country"].widget = forms.Select(
                choices=country_list
            )
        if not isinstance(
            self.fields["shipping_detail_country"].widget, forms.HiddenInput
        ):
            # Shipping country field is not hidden
            self.fields["shipping_detail_country"].widget = forms.Select(
                choices=country_list
            )

        # The card number and CCV fields should have the 'name' attribute removed
        # and the fields made non-required, as they will be handled by the javascript
        # and remain blank when hitting the server.
        if not isinstance(self.fields["card_number"].widget, forms.HiddenInput):
            # Card number is not hidden
            attrs = {
                "placeholder": "0000 0000 0000 0000",
            }
            self.fields["card_number"].widget = NoNameTextInput(attrs=attrs)
            self.fields["card_number"].required = False
        if not isinstance(self.fields["card_ccv"].widget, forms.HiddenInput):
            # Card CCV is not hidden
            attrs = {
                "placeholder": "***",
            }
            self.fields["card_ccv"].widget = NoNameTextInput(attrs=attrs)
            self.fields["card_ccv"].required = False

    def clean(self):
        """
        See if the payment form returned any errors
        See if the payment_method_nonce was created successfully.
        """
        if self.cleaned_data["step"] >= checkout.CHECKOUT_STEP_PAYMENT:
            if self.fields["payment_method"].value == "card":
                braintree_errors = self.cleaned_data["braintree_errors"]
                if braintree_errors:
                    errors = json.loads(braintree_errors)
                    if "cardNumber" in errors and errors["cardNumber"] == "blank":
                        self._errors["card_number"] = self.error_class(
                            [_("This field is required.")]
                        )
                    elif (
                        "cardNumber" in errors
                        and errors["cardNumber"] == "invalid_type"
                    ):
                        self._errors["card_number"] = self.error_class(
                            [_("This card is not supported.")]
                        )
                    elif "cardNumber" in errors and errors["cardNumber"] == "invalid":
                        self._errors["card_number"] = self.error_class(
                            [_("A valid card number is required.")]
                        )
                    if "cardExpiry" in errors and errors["cardExpiry"] == "invalid":
                        self._errors["card_expiry_year"] = self.error_class(
                            [_("A valid expiry date is required.")]
                        )
                    if "cardCCV" in errors and errors["cardCCV"] == "blank":
                        self._errors["card_ccv"] = self.error_class(
                            [_("This field is required.")]
                        )
                    elif "cardCCV" in errors and errors["cardCCV"] == "invalid":
                        self._errors["card_ccv"] = self.error_class(
                            [_("A valid CCV is required.")]
                        )
                    if "tokenizeCard" in errors and errors["tokenizeCard"] == "failed":
                        raise forms.ValidationError(
                            _(
                                "Credit Card Number/CCV could not be processed. Please try again."
                            )
                        )
                elif not self.cleaned_data["payment_method_nonce"]:
                    # Payment Method Nonce is blank, but braintree_errors is
                    # also blank - this may occur if e.g. javascript is disabled.
                    # Although we have warnings in place (see braintreejs.html and
                    # payment.html) we should catch this here rather than later.
                    raise forms.ValidationError(
                        _(
                            "Credit Card Number/CCV could not be processed. Please try again."
                        )
                    )

        return super().clean()
