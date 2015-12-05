from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets

from dataset.models import Dataset
from dataset.serializers import DatasetSerializer

class DatasetAPIList(generics.ListAPIView):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer

class DatasetAPIDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_object(self):
        acc_num = self.kwargs.get('acc_num')
        if acc_num:
            try:
                obj = Dataset.objects.get(accession_number=acc_num)
            except queryset.model.DoesNotExist:
                raise Http404(_("No %(verbose_name)s found matching the query") %
                              {'verbose_name': queryset.model._meta.verbose_name})
            return obj
        else:
            return super(DatasetAPIDetail, self).get_object()
