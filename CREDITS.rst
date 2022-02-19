CREDITS
=======

*  Danny Sag (molokov): Initial author

*  Henri Hulski:

   - Rewriting the app to match the new v.zero API.
   - Add client-side card validation.
   - Refactor country support.
   - Include PayPal payments.
   - Make it a full PyPI package.

* ryneeverett

* ianaré sévi

*  Stripe:

   Cartridge_braintree is using `jquery.payment`_ from stripe
   for client-side credit card validation and number formatting.

   .. _jquery.payment: https://github.com/stripe-archive/jquery.payment

*  Chris Beaven:

   The country selection is based on django-countries_.
   Cartridge_braintree uses also the translations of country names
   from django-countries.

   .. _django-countries: https://github.com/SmileyChris/django-countries
