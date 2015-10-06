from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView

from dataset.forms import DatasetForm
from dataset.models import Dataset

class DatasetList(ListView):
    model = Dataset

class DatasetCreate(CreateView):
    model = Dataset
    form_class = DatasetForm
    success_url = reverse_lazy('dataset_list')

class DatasetUpdate(UpdateView):
    model = Dataset
    form_class = DatasetForm
    success_url = reverse_lazy('dataset_list')
