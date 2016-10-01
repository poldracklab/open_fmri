from django.conf.urls import patterns, url

from dataset.views import (DatasetCreateUpdate, DatasetDelete,
    DatasetDetail, DatasetList, FeaturedDatasetEdit,
    FeaturedDatasetDelete, UserDatasetCreate, UserDataRequestCreate,
    UserDataset, ReferencePaperCreate, ReferencePaperUpdate,
    ReferencePaperDelete, ReferencePaperList)

from dataset.api_views import DatasetAPIList, DatasetAPIDetail

urlpatterns = patterns('',
    url(
        r'^new/$',
        DatasetCreateUpdate.as_view(),
        name='dataset_create'
    ),
    url(
        r'^edit/(?P<pk>ds\d+[a-zA-Z]?)$',
        DatasetCreateUpdate.as_view(),
        name='dataset_update'
    ),
    # this url maintains backwards compatability with old site detail view
    url(
        r'^(?P<pk>ds\d+[a-zA-Z]?)/$',
        DatasetDetail.as_view(),
        name='dataset_detail'
    ),
    url(
        r'^delete/(?P<pk>ds\d+[a-zA-Z]?)$', 
        DatasetDelete.as_view(), 
        name='dataset_delete'
    ),
    url(
        r'^featured/$',
        FeaturedDatasetEdit.as_view(), 
        name='featureddataset_edit'
    ),
    url(
        r'^featured/delete/(?P<pk>\d+)$', 
        FeaturedDatasetDelete.as_view(),
        name='featureddataset_delete'
    ),
    url(
        r'^user_data_request/new/$',
        UserDataRequestCreate.as_view(),
        name='user_data_request'
    ),
    url(
        r'^user/new/(?P<token>.*)/$',
        UserDatasetCreate.as_view(),
        name='user_create_dataset'
    ),
    url(
        r'^user/(?P<token>.*)/$',
        UserDataset.as_view(),
        name='user_dataset'
    ),
    url(
        r'^reference/$',
        ReferencePaperList.as_view(),
        name='reference_paper_list'
    ),
    url(
        r'^reference/new/$',
        ReferencePaperCreate.as_view(),
        name='reference_paper_create'
    ),
    url(
        r'^reference/edit/(?P<pk>\d+)$',
        ReferencePaperUpdate.as_view(),
        name='reference_paper_update'
    ),
    url(
        r'^reference/delete/(?P<pk>\d+)$',
        ReferencePaperDelete.as_view(),
        name='reference_paper_delete'
    ),
    url(
        r'^$',
        DatasetList.as_view(),
        name='dataset_list'
    ),
)

urlpatterns += patterns('',
    url(
        r'^api/$',
        DatasetAPIList.as_view(),
        name='dataset_api_list'
    ),
    url(
        r'^api/(?P<pk>ds\d+[a-zA-Z]?)/$',
        DatasetAPIDetail.as_view(),
        name='dataset_api_detail'
    ),
)
