from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.paging.page, name='main.views.home'),

    url(r'^view/(?P<post_id>\d+)$', views.thread.view, name='main.views.thread.view'),
    url(r'^new$', views.thread.new, name='main.views.thread.new'),

    url(r'^raw/(?P<post_id>\d+)$', views.post.raw, name='main.views.post.raw'),
    url(r'^edit/(?P<post_id>\d+)$', views.post.edit, name='main.views.post.edit'),
    url(r'^del/(?P<post_id>\d+)$', views.post.delete, name='main.views.post.delete'),
    url(r'^h/(?P<post_id>\d+)$', views.post.history, name='main.views.post.history'),

    url(r'^tags$', views.tag.index, name='main.views.tag.index'),
    url(r'^tag/(?P<pattern>(~?\w+)(\|~?\w+)*)$', views.tag.search, name='main.views.tag.search'),

    url(r'^search$', views.search.search, name='main.views.search.search'),

    url(r'^about$', views.about.about, name='main.views.about.about'),
    url(r'^markdown$', views.about.markdown, name='main.views.about.markdown'),
    url(r'^render$', views.about.render_markdown, name='main.views.about.render_makdown'),
]
