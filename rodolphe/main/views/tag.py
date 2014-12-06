from django.shortcuts import render_to_response
from django.db.models import Q
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.translation import ugettext as _

from main.models import Post, Tag
from main.forms import PostForm

import re
from collections import defaultdict


def index(request):
    indexed_tags = defaultdict(list)
    for tag in Tag.objects.all():
        first_letter = tag.name[0].upper()
        indexed_tags[first_letter].append(tag.name)
    sorted_tags = []
    for letter, tags in sorted(indexed_tags.items()):
        sorted_tags.append((letter, sorted(tags)))
    context = RequestContext(request, {
        'indexed_tags': sorted_tags
    })
    return render_to_response('tags.html', context)


def search(request, pattern):
    tag = re.escape('.{}'.format(pattern))
    q = Q(content__iregex=r'(\s|\A){}(\W|\Z)'.format(tag))
    paginator = Paginator(Post.objects.filter(q, active=True)
                          .order_by('-last_resp_at'), 10)
    page_id = request.GET.get('page')
    try:
        posts = paginator.page(page_id)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = RequestContext(request, {
        'page': posts,
        'form': PostForm(),
        'title': '{} - {}'.format(_('tag'), pattern)
    })
    return render_to_response('index.html', context)
