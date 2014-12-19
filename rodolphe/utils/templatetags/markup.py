from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

from main.models import Post

import markdown

register = template.Library()


class DisableImagesExtension(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        del md.inlinePatterns['image_link']
        del md.inlinePatterns['image_reference']
disable_images = DisableImagesExtension()


class MoreStyleExtension(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        del_tag = markdown.inlinepatterns.SimpleTagPattern(r'(--)(.*?)--',
                                                           'del')
        md.inlinePatterns.add('del', del_tag, '>not_strong')
        u_tag = markdown.inlinepatterns.SimpleTagPattern(r'(__)(.*?)__', 'u')
        md.inlinePatterns.add('underline', u_tag, '>del')
more_style = MoreStyleExtension()


class PostReferencesPattern(markdown.inlinepatterns.Pattern):
    def handleMatch(self, m):
        try:
            post = Post.objects.get(id=int(m.group(3)), active=True)
        except Post.DoesNotExist:
            return
        a = markdown.util.etree.Element('a')
        url = reverse('main.views.thread.view', args=(post.thread.id,))
        a.set('href', '{}#p{}'.format(url, post.id))
        a.text = '#{}'.format(post.id)
        return a


class PostReferencesExtension(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        pattern = PostReferencesPattern(r'(&#)([0-9]+)')
        md.inlinePatterns.add('post_references', pattern, '_end')
post_references = PostReferencesExtension()


class DottagsPattern(markdown.inlinepatterns.Pattern):
    labels = {
        '?': 'label-info',
        '!': 'label-danger',
        '+': 'label-success',
        '~': 'label-warning'
    }
    tpl = template.loader.get_template('tag.html')

    def handleMatch(self, m):
        prev, expr, tag, dot = m.group(1), m.group(2), m.group(3), m.group(4)
        if prev and not prev[-1] in ' \t\n\r\f\v':
            return expr
        context = template.Context({'tag': tag})
        content = self.tpl.render(context).replace('\n', '')
        return markdown.util.etree.fromstring(content)


class DottagsExtension(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        pattern = DottagsPattern(r'(\.(\w+)(\?|!|\+|~)?)')
        md.inlinePatterns.add('dottags', pattern, '_begin')
dottags = DottagsExtension()


@register.filter('markdown', is_safe=True)
@stringfilter
def do_markdown(value):
    extensions = ('nl2br', disable_images, more_style, post_references, dottags)
    return mark_safe(markdown.markdown(value,
                                       extensions,
                                       safe_mode='escape',
                                       enable_attributes=False))
