from dataset.models import FeaturedDataset

def featured_dataset_processor(request):
    try:
        featured_dataset = FeaturedDataset.objects.latest('date_featured')
        return {'featured_dataset': featured_dataset}
    except FeaturedDataset.DoesNotExist:
        return {}
