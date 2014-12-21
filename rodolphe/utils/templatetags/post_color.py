from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def post_color(author):
    n = int.from_bytes(author.encode(), 'big') % 0xffffff
    mask = 0xaa
    r, g, b = (n >> 16) & mask, (n >> 8) & mask, n & mask
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)
