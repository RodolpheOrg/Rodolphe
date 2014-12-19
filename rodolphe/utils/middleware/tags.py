from django.core.urlresolvers import resolve, reverse
from django.http import HttpResponsePermanentRedirect

from utils.tags import TagsSet


class TagsMiddleware:
    view = 'main.views.tag.search'

    def process_request(self, request):
        if not any(s in request.GET
                   for s in ('add_tag', 'exclude_tag', 'del_tag')):
            return
        add_tag = request.GET.get('add_tag')
        exclude_tag = request.GET.get('exclude_tag')
        del_tag = request.GET.get('del_tag')

        url = resolve(request.path)
        if url.view_name == self.view:
            tags = TagsSet.from_string(url.kwargs.get('pattern'))
        else:
            tags = TagsSet()
        if add_tag:
            tags.add(add_tag)
        if exclude_tag:
            tags.exclude(exclude_tag)
        if del_tag:
            tags.remove(del_tag)

        new_url = reverse(self.view, args=(str(tags),))
        return HttpResponsePermanentRedirect(new_url)
