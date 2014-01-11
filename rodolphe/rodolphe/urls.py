from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'rodolphe.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'post.views.home'),
    url(r'^(?P<page_id>\d+)$', 'post.views.page'),
    url(r'^post/(?P<post_id>\d+)$', 'post.views.post'),
    url(r'^post/new$', 'post.views.new'),
    url(r'^edit/(?P<post_id>\d+)$', 'post.views.edit'),

    url(r'^admin/', include(admin.site.urls)),
)
