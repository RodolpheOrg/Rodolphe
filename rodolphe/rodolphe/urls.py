from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'post.views.page'),
    url(r'^view/(?P<post_id>\d+)$', 'post.views.view'),
    url(r'^raw/(?P<post_id>\d+)$', 'post.views.raw'),
    url(r'^new$', 'post.views.new'),
    url(r'^edit/(?P<post_id>\d+)$', 'post.views.edit'),
    url(r'^del/(?P<post_id>\d+)$', 'post.views.delete'),
    url(r'^h/(?P<post_id>\d+)$', 'post.views.history'),

    url(r'^tag/(?P<pattern>\w+)$', 'post.views.tagsearch'),

    url(r'^about$', 'post.views.about'),
    url(r'^markdown$', 'post.views.markdown'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^captcha/', include('captcha.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
