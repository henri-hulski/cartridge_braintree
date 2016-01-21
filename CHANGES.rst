CHANGES
=======

1.0b2 (2016-01-21)
------------------

This is an entire rewrite release of the whole app by Henri Hulski.

- Rewriting the app to match the new Braintree v.zero API.
- Refactor country support for billing/shipping inspired by
  `django-countries <https://github.com/SmileyChris/django-countries>`_
  and using their translations of country names.
- Add client site credit card validation and number formatting using the
  jQuery plugin from `payform <https://github.com/jondavidjohn/payform>`_.
- Include PayPal payments.
- Make it a full PyPI package.

Initial release (2013-07-28)
----------------------------

Initial release by molokov.
