from mezzanine.conf import register_setting
from cartridge_braintree.countries import get_country_names_list

register_setting(
    name="SHOP_DEFAULT_COUNTRY",
    description="Default selected country in the billing/shipping fields",
    editable=True,
    choices=zip(get_country_names_list(), get_country_names_list()),
    default="United States of America"
)

# -----------------------------------------------
# Braintree Client Side Encryption Key
# -----------------------------------------------
register_setting(
    name="BRAINTREE_CLIENT_SIDE_ENCRYPTION_KEY",
    editable=False,
    default="",
)

# -----------------------------------------------
# Make sure we can access the client side encryption key from within templates
# -----------------------------------------------
register_setting(
    name="TEMPLATE_ACCESSIBLE_SETTINGS",
    append=True,
    default=("BRAINTREE_CLIENT_SIDE_ENCRYPTION_KEY",),
)
