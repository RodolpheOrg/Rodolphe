from django.conf import settings

from main.models import Tag


def site_name(request):
    return {'SITE_NAME': getattr(settings, 'SITE_NAME', None)}


def favicon(request):
    return {'FAVICON': getattr(settings, 'FAVICON', None)}


def tags(request):
    return {
        'popular_tags': Tag.objects.order_by('-count')[:10],
        'recent_tags': Tag.objects.order_by('-id')[:10]
    }
