from django.conf import settings

from post.models import Tag


def site_name(request):
    return {'SITE_NAME': getattr(settings, 'SITE_NAME', None)}


def favicon(request):
    return {'FAVICON': getattr(settings, 'FAVICON', None)}


def popular_tags(request):
    return {'popular_tags': Tag.objects.order_by('-count')[:10]}
