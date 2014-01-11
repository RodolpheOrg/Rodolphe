from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'post.views.page'),
    url(r'^view/(?P<post_id>\d+)$', 'post.views.view'),
    url(r'^new$', 'post.views.new'),
    url(r'^edit/(?P<post_id>\d+)$', 'post.views.edit'),
    url(r'^del/(?P<post_id>\d+)$', 'post.views.delete'),

    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
