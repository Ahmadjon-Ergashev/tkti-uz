from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='add_spaces')
@stringfilter
def add_spaces(value):
    try:
        parts = value.split('.')
        parts[0] = '{:,}'.format(int(parts[0])).replace(',', ' ')
        return '.'.join(parts)
    except (ValueError, TypeError):
        return value