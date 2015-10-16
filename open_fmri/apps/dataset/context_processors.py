from dataset.models import FeaturedDataset

def featured_dataset_processor(request):
    featured_dataset = FeaturedDataset.objects.latest('date_featured')
    return {'featured_dataset': featured_dataset}
