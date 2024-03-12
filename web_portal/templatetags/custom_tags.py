from django import template

register = template.Library()

@register.filter
def get_filter_param(params, key):
    modified_key = key + '_filter'
    return params.get(modified_key, '')

@register.filter
def get_attribute(obj, attribute):
    try:
        return getattr(obj, attribute)
    except AttributeError:
        return ''