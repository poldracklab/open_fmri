from django.conf.urls import patterns, url

from dataset.views import DatasetCreate, DatasetList, DatasetUpdate

urlpatterns = patterns('',
    url(r'^new/$', DatasetCreate.as_view(), name='dataset_create'),
    url(r'^edit/(?P<pk>\d+)$', DatasetUpdate.as_view(), name='dataset_update'),
    url(r'^$', DatasetList.as_view(), name='dataset_list'),
)

