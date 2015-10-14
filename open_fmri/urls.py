from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages import views

import contact_form.urls
import dataset.urls

urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^dataset/', include(dataset.urls)),
    url(r'^contact/', include('contact_form.urls')),
    url(r'^(?P<url>.*/)$', views.flatpage),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
