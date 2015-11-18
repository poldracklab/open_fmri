from rest_framework import generics

from dataset.models import Dataset
from dataset.serializers import DatasetSerializer

class DatasetAPIList(generics.ListCreateAPIView):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer

class DatasetAPIDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
