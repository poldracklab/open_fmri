from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages import views
from django.views.generic import TemplateView

import contact.urls
import dataset.urls
from dataset.views import DatasetList, Index

urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^dataset/', include(dataset.urls)),
    url(r'^contact/', include('contact.urls')),
    url(r'^$', DatasetList.as_view()),
    url(r'^front/$', Index.as_view(), name='index'),
    url(r'^(?P<url>.*/)$', views.flatpage),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
