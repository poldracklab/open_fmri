from django.conf.urls import patterns, url

from dataset.views import DatasetCreate, DatasetDelete, DatasetDetail, \
    DatasetList, DatasetUpdate, FeaturedDatasetEdit, FeaturedDatasetDelete, \
    UserCreateDataset, UserDataRequestCreate

from dataset.api_views import DatasetAPIList, DatasetAPIDetail

urlpatterns = patterns('',
    url(r'^new/$', DatasetCreate.as_view(), name='dataset_create'),
    url(r'^edit/(?P<pk>\d+)$', DatasetUpdate.as_view(), name='dataset_update'),
    url(r'^view/(?P<pk>\d+)$', DatasetDetail.as_view(), name='dataset_detail'),
    url(r'^delete/(?P<pk>\d+)$', DatasetDelete.as_view(), 
        name='dataset_delete'),
    url(r'^featured/delete/(?P<pk>\d+)$', 
        FeaturedDatasetDelete.as_view(), name='featureddataset_delete'),
    url(r'^featured/$', FeaturedDatasetEdit.as_view(), 
        name='featureddataset_edit'),
    url(r'^user_data_request/new/$', UserDataRequestCreate.as_view(),
        name='user_data_request'),
    url(r'^new/(?P<token>.*)$', UserCreateDataset.as_view(),
        name='user_create_dataset'),
    url(r'^$', DatasetList.as_view(), name='dataset_list'),
)

urlpatterns += patterns('',
    url(r'^api/$', DatasetAPIList.as_view(), name='dataset_api_list'),
    url(r'^api/(?P<pk>\d+)$', DatasetAPIDetail.as_view(), 
        name='dataset_api_detail'),
)
