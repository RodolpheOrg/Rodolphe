from django.db.models import Q


def get_search(request):
    q = Q()
    search = {}
    extra = []
    search['advanced'] = request.GET.get('q_advanced', '')
    search['q'] = request.GET.get('q', '')
    if search['q']:
        extra.append('q')
        q &= Q(content__icontains=search['q'])
    search['q_author'] = request.GET.get('q_author', '')
    if search['q_author']:
        extra.append('q_author')
        q &= Q(author__name__icontains=search['q_author'])
    if 'q_pictures' in request.GET:
        search['q_pictures'] = request.GET['q_pictures']
        extra.append('q_pictures')
        if search['q_pictures']:
            q &= ~Q(picture='')
    if 'q_all' in request.GET:
        search['q_all'] = request.GET['q_all']
        extra.append('q_all')
    if not search.get('q_all', False):
        q &= Q(parent=None)
    search['extra'] = '&'.join('{}={}'.format(param, request.GET[param]) for param in extra)
    return q, search
