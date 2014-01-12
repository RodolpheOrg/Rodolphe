from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

import markdown

register = template.Library()


class DisableImages(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        del md.inlinePatterns['image_link']
        del md.inlinePatterns['image_reference']


@register.filter('markdown', is_safe=True)
@stringfilter
def do_markdown(value):
    extensions = ('nl2br', DisableImages())
    return mark_safe(markdown.markdown(value,
                                       extensions,
                                       safe_mode='escape',
                                       enable_attributes=False))
