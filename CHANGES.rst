CHANGES
=======

3.0.5 (2022-05-14)
--------------------

- Handle also mobile Card and PayPal buttons.
- Check payment_method from fields instead of cleaned_data.


3.0.4 (2022-05-14)
--------------------

- Prepare also hidden card and paypal buttons.


3.0.3 (2022-05-14)
--------------------

- Validate card expiry fields only if they're not hidden.
- Remove double javascript compression from braintreejs.html.
- Update translations and add error translations.


3.0.2 (2022-05-06)
--------------------

- Use Cartridge stable release 1.3+.
- State/Region fields are now already optional in Cartridge. So removing them from form.py.
- Fix CheckoutError message.


3.0.1 (2022-03-23)
--------------------

- Switch to braintree-web API v3.

BREAKING CHANGE: Some older browsers will not work anymore.
    For supported browsers see
    https://braintree.github.io/braintree-web/3.85.2/#browser-support.


2.0.0 (2022-03-23)
--------------------

- Use Cartridge stable release 1.1+.
- Switch to stable.


2.0.0b5 (2022-03-22)
--------------------

Features:
- use JavaScript compression
- remove name from card payment form

Fixes:
- fix error reporting for card expire fields
- round order_total to 2 digits
- use paypal as a modal instead of a popup

Refactor, Style and Traslation:
- clean up braintree.html javascript
- remove unused translations and English translation
- some minor style fixes


2.0.0b4 (2022-03-01)
--------------------

- Use new template tag to the get order_total amount for PayPal.


2.0.0b3 (2022-02-27)
--------------------

- Remove card type field from checkout form.
- Check if the detected card type is in SHOP_CARD_TYPES setting.
- SHOP_CARD_TYPES defaults now to all cards which are supported by Braintree.
- Make state/region fields optional.
- Rearrange field order.
- Update translations.


2.0.0b2 (2022-02-26)
--------------------

- Bugfix: update signature for the NoNameTextInput widget render method.
- Upgrade Braintree.js SDK to 2.32.1.


2.0.0b1 (2022-02-19)
--------------------

This is a service release which has breaking changes for dependencies.

- Upgrade to Cartridge 1.0+ (for now we use the repo at henri-hulski/cartridge).
- Using Mezannine 5.1+.
- Supporting Django 3.2 and 4.0.
- Drop Python support for Python 2 and support only Python 3.7+.
- Adding Code style tools: black, flake8, isort and pyupgrade.


1.2.2 (2021-04-19)
------------------

- Set minimum Django version to 1.11.29 and maximum version under 1.12
  to fix security vulnerabilities.


1.2.1 (2019-12-28)
------------------

- Upgrade to Django 1.11 and Cartridge 0.13.


1.1.0 (2016-10-21)
------------------

- Add logging to payment process. [ianare]
- **Breaking change**: Add ``SHOP_DEFAULT_COUNTRY`` setting and by default
  force the user to select a country (set to ``True`` for v1.0.0 behavior). [ianare]


1.0.0 (2016-07-08)
------------------

- **Breaking change**: Simplify urls setup. [ryneeverett]

  When upgrading to 1.0.0 change cartridge_braintree urls in ``urls.py`` to::

     url("^shop/(?=checkout(/?)$)", include("cartridge_braintree.urls")),

- Make it a stable release version as it's already well tested.
- Introduce `semantic versioning`_.
- Use zest.releaser for release.

.. _semantic versioning: http://semver.org

1.0b17 (2016-04-17)
-------------------

- Upgrade jquery.payment.js to v1.3.3. [ryneeverett]

1.0b16 (2016-04-17)
-------------------

- Fix documentation bug.
  It should be ``BRAINTREE_MERCHANT_ID`` not ``BRAINTREE_MERCHANT``
  in ``settings.py``.

1.0b16 (2016-04-17)
-------------------

- Fix documentation bug.
  It should be ``BRAINTREE_MERCHANT_ID`` not ``BRAINTREE_MERCHANT``
  in ``settings.py``.

1.0b14 (2016-03-14)
-------------------

- Replace the payform jQuery plugin with
  jquery.payment <https://github.com/stripe-archive/jquery.payment>
  from stripe.
  This fixes some bugs with card number and CCV formatting.

1.0b13 (2016-02-03)
-------------------

- Move static content to subfolder.
- Clean up translation files.
- Minor fixes and javascript optimizations.

1.0b10 (2016-01-30)
-------------------

- Overextents templates instead of overriding them.
- Show Card payment form when Django returns errors.
- Add placeholders for card number and CCV
  and trigger numeric keyboard on iPhone.
- Add dependency on Cartridge 0.11.
  Drop support for older Cartridge versions.
- Minor fixes.

1.0b8 (2016-01-25)
------------------

- Upgrade to Cartridge 0.11.
- Clean up the template directory.

1.0b4 (2016-01-21)
------------------

This is an entire rewrite release of the whole app by Henri Hulski.

- Rewriting the app to match the new Braintree v.zero API.
- Refactor country support for billing/shipping inspired by
  `django-countries <https://github.com/SmileyChris/django-countries>`_.
  and using their translations of country names.
- Add client site credit card validation and number formatting using the
  jQuery plugin from `payform <https://github.com/jondavidjohn/payform>`_.
- Include PayPal payments.
- Add country names translations from django-countries.
  Full translation of the app for German, French and Polish.
- Change license from MIT to BSD.
- Make it a full PyPI package.

Initial release (2013-07-28)
----------------------------

Initial release by Danny Sag (molokov).
