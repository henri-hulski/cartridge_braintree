from mezzanine.conf import register_setting

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
