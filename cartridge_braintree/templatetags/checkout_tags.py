from cartridge.shop.templatetags.shop_tags import _order_totals
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def get_order_total(context):
    """Off-canvas version of order_totals."""
    order_totals = _order_totals(context)
    return mark_safe(order_totals["order_total"])
