from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'main.views.paging.page'),

    url(r'^view/(?P<post_id>\d+)$', 'main.views.thread.view'),
    url(r'^new$', 'main.views.thread.new'),

    url(r'^raw/(?P<post_id>\d+)$', 'main.views.post.raw'),
    url(r'^edit/(?P<post_id>\d+)$', 'main.views.post.edit'),
    url(r'^del/(?P<post_id>\d+)$', 'main.views.post.delete'),
    url(r'^h/(?P<post_id>\d+)$', 'main.views.post.history'),

    url(r'^tags$', 'main.views.tag.index'),
    url(r'^tag/(?P<pattern>(~?\w+)(\|~?\w+)*)$', 'main.views.tag.search'),

    url(r'^search$', 'main.views.search.search'),

    url(r'^about$', 'main.views.about.about'),
    url(r'^markdown$', 'main.views.about.markdown'),
    url(r'^render$', 'main.views.about.render'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^captcha/', include('captcha.urls')),

    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt',
                                               content_type='text/plain'))
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
