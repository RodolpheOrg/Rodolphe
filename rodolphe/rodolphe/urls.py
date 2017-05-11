from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'', include('main.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^captcha/', include('captcha.urls')),

    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt',
                                               content_type='text/plain'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
