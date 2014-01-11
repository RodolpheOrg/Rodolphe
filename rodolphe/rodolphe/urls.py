from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'post.views.page'),
    url(r'^view/(?P<post_id>\d+)$', 'post.views.view'),
    url(r'^new$', 'post.views.new'),
    url(r'^edit/(?P<post_id>\d+)$', 'post.views.edit'),

    url(r'^admin/', include(admin.site.urls)),
)
