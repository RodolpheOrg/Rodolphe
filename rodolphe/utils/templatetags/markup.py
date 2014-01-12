from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

import markdown

register = template.Library()


class DisableImagesExtension(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        del md.inlinePatterns['image_link']
        del md.inlinePatterns['image_reference']
disable_images = DisableImagesExtension()

class MoreStyleExtension(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        del_tag = markdown.inlinepatterns.SimpleTagPattern(r'(--)(.*?)--', 'del')
        md.inlinePatterns.add('del', del_tag, '>not_strong')
        u_tag = markdown.inlinepatterns.SimpleTagPattern(r'(__)(.*?)__', 'u')
        md.inlinePatterns.add('underline', u_tag, '>del')
more_style = MoreStyleExtension()

class PostReferencesPattern(markdown.inlinepatterns.Pattern):
    def handleMatch(self, m):
        a = markdown.util.etree.Element('a')
        a.set('href', '#p{}'.format(m.group(3)))
        a.text = '#{}'.format(m.group(3))
        return a
class PostReferencesExtension(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        pattern = PostReferencesPattern(r'(&#)([0-9]+)')
        md.inlinePatterns.add('post_references', pattern, '_end')
post_references = PostReferencesExtension()

@register.filter('markdown', is_safe=True)
@stringfilter
def do_markdown(value):
    extensions = ('nl2br', disable_images, more_style, post_references)
    return mark_safe(markdown.markdown(value,
                                       extensions,
                                       safe_mode='escape',
                                       enable_attributes=False))
