from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages import views
from django.views.generic.base import RedirectView, TemplateView

import contact.urls
import dataset.urls
from dataset.views import DatasetList, Index

urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^dataset/', include(dataset.urls)),
    url(r'^contact/', include('contact.urls')),
    url(r'^data-organization/', 
        RedirectView.as_view(url='http://bids.neuroimaging.io', permanent=True),
        name='data-organization'),
    url(r'^$', Index.as_view(), name='index'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^subscribed/', TemplateView.as_view(template_name='subscribe_success.html')),
    url(r'^(?P<url>.*/)$', views.flatpage),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
