from django.utils.encoding import force_str
from mezzanine.conf import settings

from cartridge_braintree.countries import COUNTRIES

try:
    import pyuca
except ImportError:
    pyuca = None

# Use UCA sorting if it's available.
if pyuca:
    collator = pyuca.Collator()
    sort_key = lambda item: collator.sort_key(item[1])
else:
    import unicodedata

    # Cheap and dirty method to sort against ASCII characters only.
    sort_key = lambda item: (
        unicodedata.normalize("NFKD", item[1]).encode("ascii", "ignore").decode("ascii")
    )


def get_first_country():
    """
    Get a list of the first country
    """
    if not settings.SHOP_DEFAULT_COUNTRY:
        return [("", "")]
    # don't simplify, 'True' has a specific meaning here
    elif settings.SHOP_DEFAULT_COUNTRY is not True:
        return [get_country(settings.SHOP_DEFAULT_COUNTRY)]
    else:
        return []


def get_country_list():
    """
    Get a sorted list of tuples with 2 elements in the form of
    (alpha2, translated_country_name) for the countries set in
    SHOP_SUPPORTED_COUNTRIES or if not set for all countries
    Braintree supports.
    The countries in SHOP_PRIMARY_COUNTRIES get moved at the beginning.
    Used for the checkout form to make Country a drop down list
    """
    primary_countries = []
    if settings.SHOP_PRIMARY_COUNTRIES:
        primary_countries = [
            get_country(country)
            for country in settings.SHOP_PRIMARY_COUNTRIES
            if country is not settings.SHOP_DEFAULT_COUNTRY
        ]
        primary_countries = sorted(primary_countries, key=sort_key)

    if settings.SHOP_SUPPORTED_COUNTRIES:
        country_list = [
            get_country(country)
            for country in settings.SHOP_SUPPORTED_COUNTRIES
            if country not in settings.SHOP_PRIMARY_COUNTRIES
            and country is not settings.SHOP_DEFAULT_COUNTRY
        ]

    else:
        country_list = [
            (code, force_str(name))
            for code, name in COUNTRIES.items()
            if code not in settings.SHOP_PRIMARY_COUNTRIES
            and code is not settings.SHOP_DEFAULT_COUNTRY
        ]

    return get_first_country() + primary_countries + sorted(country_list, key=sort_key)


def get_country(country):
    """
    Get the country tuple in the form of (alpha2, local_name)
    for given alpha2 country code
    """
    if country and isinstance(country, str):
        return country, force_str(COUNTRIES[country])
    else:
        # country is either empty or already a tuple so leave it unchanged
        return country
