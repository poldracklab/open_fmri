from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from dataset.forms import DatasetForm, InvestigatorFormSet, \
    PublicationDocumentFormSet, PublicationFullTextFormSet, \
    PublicationPubMedLinkFormSet, TaskFormSet
from dataset.models import Dataset, Investigator, PublicationDocument, \
    PublicationFullText, PublicationPubMedLink

class DatasetList(ListView):
    model = Dataset

class DatasetDelete(DeleteView):
    model = Dataset
    success_url = reverse_lazy('dataset_list')

class DatasetCreate(CreateView):
    model = Dataset
    form_class = DatasetForm
    success_url = reverse_lazy('dataset_list')

    def get_context_data(self, **kwargs):
        context = super(DatasetCreate, self).get_context_data(**kwargs)
        context['investigator_formset'] = InvestigatorFormSet()
        context['publication_document_formset'] = PublicationDocumentFormSet()
        context['publication_full_text_formset'] = PublicationFullTextFormSet()
        context['publication_pubmed_link_formset'] = \
            PublicationPubMedLinkFormSet()
        context['task_formset'] = TaskFormSet()
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
            investigator_formset.save()
        
        publication_full_text_formset = PublicationFullTextFormSet(
            self.request.POST, self.request.FILES, instance=dataset)

        if publication_full_text_formset.is_valid():
            publication_full_text_formset.save()

        publication_pubmed_link_formset = PublicationPubMedLinkFormSet(
            self.request.POST, instance=dataset)

        if publication_pubmed_link_formset.is_valid():
            publication_pubmed_link_formset.save()

        return super(DatasetCreate, self).form_valid(form)

class DatasetUpdate(UpdateView):
    model = Dataset
    form_class = DatasetForm
    success_url = reverse_lazy('dataset_list')

    def get_context_data(self, **kwargs):
        context = super(DatasetUpdate, self).get_context_data(**kwargs)
        context['investigator_formset'] = InvestigatorFormSet(
            instance=self.object)
        context['publication_document_formset'] = PublicationDocumentFormSet(
            instance=self.object)
        context['publication_full_text_formset'] = PublicationFullTextFormSet(
            instance=self.object)
        context['publication_pubmed_link_formset'] = \
            PublicationPubMedLinkFormSet(instance=self.object)
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
            investigator_formset.save()
        
        publication_full_text_formset = PublicationFullTextFormSet(
            self.request.POST, self.request.FILES, instance=dataset)

        if publication_full_text_formset.is_valid():
            publication_full_text_formset.save()

        publication_pubmed_link_formset = PublicationPubMedLinkFormSet(
            self.request.POST, instance=dataset)

        if publication_pubmed_link_formset.is_valid():
            publication_pubmed_link_formset.save()

        return super(DatasetUpdate, self).form_valid(form)

