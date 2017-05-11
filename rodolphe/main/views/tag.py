from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.translation import ugettext as _

from main.models import Post, Tag
from main.forms import PostForm
from utils.search import get_search
from utils.tags import TagsSet

import re
from collections import defaultdict
from urllib.parse import urlencode


def index(request):
    indexed_tags = defaultdict(list)
    for tag in Tag.objects.all():
        first_letter = tag.name[0].upper()
        indexed_tags[first_letter].append(tag.name)
    sorted_tags = []
    for letter, tags in sorted(indexed_tags.items()):
        sorted_tags.append((letter, sorted(tags)))
    return render(request, 'tags.html', {'indexed_tags': sorted_tags})


def search(request, pattern):
    tags = TagsSet.from_string(pattern)
    q, search = get_search(request)
    regex = r'(\s|\A)\.{}(\W|\Z)'
    for tag in tags:
        q &= Q(content__iregex=regex.format(re.escape(tag)))
    for tag in tags.iter_exclude():
        q &= ~Q(content__iregex=regex.format(re.escape(tag)))
    paginator = Paginator(Post.objects.filter(q, active=True)
                          .order_by('-created_at'), 10)
    page_id = request.GET.get('page')
    try:
        posts = paginator.page(page_id)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        'page': posts,
        'form': PostForm(),
        'title': '{} - {}'.format(_('tag'), pattern),
        'search': search
    }
    return render(request, 'index.html', context)
