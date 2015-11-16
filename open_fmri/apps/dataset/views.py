import requests
import requests_cache

from django import forms
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.utils.crypto import constant_time_compare, salted_hmac
from django.views.generic import CreateView, DeleteView, DetailView, \
    ListView, UpdateView

from braces.views import LoginRequiredMixin

from dataset.forms import DatasetForm, FeaturedDatasetForm, \
    InvestigatorFormSet, InvestigatorFormSetHelper, \
    PublicationDocumentFormSet, PublicationDocumentFormSetHelper, \
    PublicationPubMedLinkFormSet, PublicationPubMedLinkFormSetHelper, \
    RevisionFormSet, RevisionFormSetHelper, TaskFormSet, TaskFormSetHelper, \
    UserDatasetForm, UserDataRequestForm
from dataset.models import Dataset, Investigator, PublicationDocument, \
    PublicationPubMedLink, FeaturedDataset, UserDataRequest

requests_cache.install_cache('test_cache')

class DatasetList(ListView):
    model = Dataset
    def get_queryset(self, **kwargs):
        if not self.request.user.is_authenticated():
            queryset = Dataset.objects.filter(status='PUBLISHED')
            return queryset
        else:
            return super(DatasetList, self).get_queryset(**kwargs)

class DatasetDelete(LoginRequiredMixin, DeleteView):
    model = Dataset
    success_url = reverse_lazy('dataset_list')

class DatasetDetail(DetailView):
    model = Dataset
    
    def get_context_data(self, **kwargs):
        context = super(DatasetDetail, self).get_context_data(**kwargs)
        context['revisions'] = self.object.revision_set.order_by('-date_set')
        return context

class DatasetCreate(LoginRequiredMixin, CreateView):
    model = Dataset
    form_class = DatasetForm
    success_url = reverse_lazy('dataset_list')

    def get_context_data(self, **kwargs):
        context = super(DatasetCreate, self).get_context_data(**kwargs)
        context['investigator_formset'] = InvestigatorFormSet()
        context['investigator_formset_helper'] = InvestigatorFormSetHelper()
        context['publication_document_formset'] = PublicationDocumentFormSet()
        context['publication_document_formset_helper'] = \
            PublicationDocumentFormSetHelper()
        context['publication_pubmed_link_formset'] = \
            PublicationPubMedLinkFormSet()
        context['publication_pubmed_link_formset_helper'] = \
            PublicationPubMedLinkFormSetHelper()
        context['task_formset'] = TaskFormSet()
        context['task_formset_helper'] = TaskFormSetHelper()
        context['revision_formset'] = RevisionFormSet(instance=self.object)
        context['revision_formset_helper'] = RevisionFormSetHelper()
        return context

    def form_valid(self, form):
        dataset = form.save()
        
        investigator_formset = InvestigatorFormSet(self.request.POST,
            self.request.FILES, instance=dataset)
        if investigator_formset.is_valid():
            investigator_formset.save()

        publication_document_formset = PublicationDocumentFormSet(
            self.request.POST, self.request.FILES, instance=dataset)
        if publication_document_formset.is_valid():
            publication_document_formset.save()

        publication_pubmed_link_formset = PublicationPubMedLinkFormSet(
            self.request.POST, instance=dataset)
        if publication_pubmed_link_formset.is_valid():
            publication_pubmed_link_formset.save()

        revision_formset = RevisionFormSet(self.request.POST, 
            instance=dataset)
        if revision_formset.is_valid():
            revision_formset.save()
        
        task_formset = TaskFormSet(self.request.POST, self.request.FILES,
            instance=dataset)
        if task_formset.is_valid():
            task_formset.save()
        
        return super(DatasetCreate, self).form_valid(form)

class DatasetUpdate(LoginRequiredMixin, UpdateView):
    model = Dataset
    form_class = DatasetForm
    success_url = reverse_lazy('dataset_list')

    def get_context_data(self, **kwargs):
        context = super(DatasetUpdate, self).get_context_data(**kwargs)
        context['investigator_formset'] = InvestigatorFormSet(
            instance=self.object)
        context['investigator_formset_helper'] = InvestigatorFormSetHelper()
        context['publication_document_formset'] = PublicationDocumentFormSet(
            instance=self.object)
        context['publication_document_formset_helper'] = \
            PublicationDocumentFormSetHelper()
        context['publication_pubmed_link_formset'] = \
            PublicationPubMedLinkFormSet(instance=self.object)
        context['publication_pubmed_link_formset_helper'] = \
            PublicationPubMedLinkFormSetHelper()
        context['task_formset'] = TaskFormSet(instance=self.object)
        context['task_formset_helper'] = TaskFormSetHelper()
        context['revision_formset'] = RevisionFormSet(instance=self.object)
        context['revision_formset_helper'] = RevisionFormSetHelper()
        return context

    def form_valid(self, form):
        dataset = form.save()
        
        investigator_formset = InvestigatorFormSet(self.request.POST,
            self.request.FILES, instance=self.object)
        if investigator_formset.is_valid():
            investigator_formset.save()

        publication_document_formset = PublicationDocumentFormSet(
            self.request.POST, self.request.FILES, instance=self.object)
        if publication_document_formset.is_valid():
            publication_document_formset.save()
        
        publication_pubmed_link_formset = PublicationPubMedLinkFormSet(
            self.request.POST, instance=self.object)
        if publication_pubmed_link_formset.is_valid():
            publication_pubmed_link_formset.save()

        revision_formset = RevisionFormSet(self.request.POST, 
            instance=self.object)
        if revision_formset.is_valid():
            revision_formset.save()
        
        task_formset = TaskFormSet(self.request.POST, self.request.FILES,
            instance=self.object)
        if task_formset.is_valid():
            task_formset.save()
        else:
            form_empty_permitted = task_formset.forms[-1].empty_permitted
            form_has_changed = task_formset.forms[-1].changed_data
            total_forms = task_formset.total_form_count()
            raise forms.ValidationError(task_formset.errors)
            
        return super(DatasetUpdate, self).form_valid(form)

class FeaturedDatasetEdit(LoginRequiredMixin, CreateView):
    model = FeaturedDataset
    form_class = FeaturedDatasetForm
    success_url = reverse_lazy('dataset_list')

    def get_context_data(self, **kwargs):
        context = super(FeaturedDatasetEdit, self).get_context_data(**kwargs)
        context['featured_datasets'] = FeaturedDataset.objects.order_by(
            '-date_featured')
        return context

class FeaturedDatasetDelete(LoginRequiredMixin, DeleteView):
    model = FeaturedDataset
    success_url = reverse_lazy('dataset_list')

class UserDataRequestCreate(LoginRequiredMixin, CreateView):
    model = UserDataRequest
    form_class = UserDataRequestForm
    success_url = reverse_lazy('dataset_list')

class UserCreateDataset(CreateView):
    model = Dataset
    form_class = UserDatasetForm
    success_url = reverse_lazy('dataset_list')
    template_name = "dataset/user_dataset_form.html"

    def dispatch(self, *args, **kwargs):
        token = self.kwargs.get('token') 
        user_data_request = get_object_or_404(UserDataRequest, token=token)
        return super(UserCreateDataset, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.save()
        # Could email the admin back here
        return super(UserDatasetCreate, self).form_valid(form)
