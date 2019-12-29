from django import template
register = template.Library()
@register.filter
def zfill_id(obj):
    return str(obj).zfill(5)


@register.filter
def limit_4(obj):
    return obj[:4]