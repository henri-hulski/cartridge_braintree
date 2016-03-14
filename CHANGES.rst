CHANGES
=======

1.0b13 (2016-02-03)
------------------

- Move static content to subfolder.
- Clean up translation files.
- Minor fixes and javascript optimizations.

1.0b10 (2016-01-30)
------------------

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
