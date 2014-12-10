from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import get_language
from django.utils.translation import ugettext as _


def about(request):
    tpl_name = 'about_{}.html'.format(get_language().split('-')[0])
    return render_to_response(tpl_name, RequestContext(request))


def markdown(request):
    examples = [
        (_("emphasis"), "*abcd*"),
        (_("emphasis"), "_abcd_"),
        (_("bold"), "**abcd**"),
        (_("underline"), "__abcd__"),
        (_("strike"), "--abcd--"),
        (_("link"), "<http://google.fr>"),
        (_("link"), "[google](http://google.fr)"),
        (_("post reference"), "&#1"),
        (_("tags"), ".tag\n.info?\n.danger!\n.success+\n.warning~"),
        (_("list"), "* a\n* b\n    * c\n* d"),
        (_("ordered list"), "1. a\n2. b"),
        (_("title"), "# Title1\n## Title 2\n### Title 3\n#### Title 4\n"
         "##### Title5\n###### Title 6"),
        (_("title"), "Title 1\n=======\n\nTitle 2\n-------"),
        (_("quotation"), "> quote\n>> subquote"),
        (_("code"), "`abcd`"),
        (_("blockcode"), "    abcd\n    efgh"),
        (_("linebreak"), "------------")
    ]
    context = RequestContext(request, {
        'examples': examples
    })
    return render_to_response('markdown.html', context)


@require_POST
@csrf_exempt
def render(request):
    context = RequestContext(request, {
        'content': request.POST.get('content', '')
    })
    return render_to_response('render.html', context)
