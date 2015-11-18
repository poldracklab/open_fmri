from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets

from dataset.models import Dataset
from dataset.serializers import DatasetSerializer

class DatasetAPIList(generics.ListAPIView):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
