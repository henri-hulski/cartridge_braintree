CREDITS
=======

*  Danny Sag (molokov): Initial author

*  Henri Hulski:

   - Rewriting the app to match the new v.zero API.
   - Add client-side card validation.
   - Refactor country support.
   - Include PayPal payments.
   - Make it a full PyPI package.

*  Jonathan D. Johnson:

   Cartridge_braintree is using the jQuery plugin from payform_
   for client-side credit card validation and number formatting.
   
   .. _payform: https://github.com/jondavidjohn/payform

*  Chris Beaven:

   The country selection is based on django-countries_.
   Cartridge_braintree uses also the translations of country names
   from django-countries.
   
   .. _django-countries: https://github.com/SmileyChris/django-countries
