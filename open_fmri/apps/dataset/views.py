import requests
import requests_cache
from urllib.parse import urlparse

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.crypto import constant_time_compare, salted_hmac
from django.views.generic import (CreateView, DeleteView, DetailView,
    ListView, UpdateView, TemplateView, View)
from django.views.generic.edit import ModelFormMixin, ProcessFormView 
from django.views.generic.detail import SingleObjectTemplateResponseMixin

from braces.views import LoginRequiredMixin

from dataset.forms import (ContactForm, ContactFormSet, ContactFormSetHelper,
    DatasetForm, FeaturedDatasetForm, InvestigatorFormSet,
    InvestigatorFormSetHelper, LinkFormSet, LinkFormSetHelper,
    PublicationDocumentFormSet, PublicationDocumentFormSetHelper,
    PublicationPubMedLinkFormSet, PublicationPubMedLinkFormSetHelper, 
    RevisionFormSet, RevisionFormSetHelper, TaskFormSet, TaskFormSetHelper,
    UserDatasetForm, UserDataRequestForm, NewContactForm, ReferencePaperForm)
from dataset.models import (Dataset, Investigator, PublicationDocument,
    PublicationPubMedLink, FeaturedDataset, UserDataRequest, ReferencePaper)
from log_parse.models import S3File

requests_cache.install_cache('cache')

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
            return super(DatasetDetail, self).get_object()

    def get_context_data(self, **kwargs):
        context = super(DatasetDetail, self).get_context_data(**kwargs)
        context['revisions'] = self.object.revision_set.order_by('-date_set')

        revisions = self.object.revision_set.order_by('-date_set')
        context_revisions = []
        for revision in revisions:
            context_links = []
            for link in revision.link_set.all().order_by('title'):
                try:
                    filename = urlparse(link.url).path 
                    if filename[0] == '/':
                        filename = filename[1:]
                    count = S3File.objects.get(filename=filename).count
                    context_links.append((link, count))
                except ObjectDoesNotExist:
                    context_links.append((link, -1))
            context_revisions.append((revision, context_links))
        
        context_links = []
        links = self.object.link_set.filter(revision__isnull=True).order_by('title')
        for link in links:
            try:
                filename = urlparse(link.url).path 
                if filename[0] == '/':
                    filename = filename[1:]
                count = S3File.objects.get(filename=filename).count
                context_links.append((link, count))
            except ObjectDoesNotExist:
                context_links.append((link, -1))
        
        context['links'] = context_links
        context['revisions'] = context_revisions
        context['other_links'] = context_links
        context['ref_papers'] = self.object.referencepaper_set.all()
        return context


class DatasetCreateUpdate(LoginRequiredMixin, SingleObjectTemplateResponseMixin,
                              ModelFormMixin, ProcessFormView):
    model = Dataset
    form_class = DatasetForm
    success_url = reverse_lazy('dataset_list')
    template_name = 'dataset/dataset_form.html'

    def get_object(self, queryset=None):
        try:
            return super(DatasetCreateUpdate, self).get_object(queryset)
        except AttributeError:
            return None

    def get(self, *args, **kwargs):
        self.object = self.get_object()
        return super(DatasetCreateUpdate, self).get(self.request, *args, **kwargs)

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        return super(DatasetCreateUpdate, self).post(self.request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DatasetCreateUpdate, self).get_context_data(**kwargs)
        contact_pk = 0
        if self.object and self.object.contact:
            contact_pk = self.object.contact.pk
        context['contact_form'] = ContactForm(
            initial = {'contact': contact_pk}
        )
        context['investigator_formset'] = InvestigatorFormSet()
        context['investigator_formset_helper'] = InvestigatorFormSetHelper()
        context['link_formset'] = LinkFormSet(instance=self.object)
        context['link_formset_helper'] = LinkFormSetHelper()
        context['new_contact_form'] = NewContactForm()
        context['publication_document_formset'] = PublicationDocumentFormSet(instance=self.object)
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
        context['contact_formset'] = ContactFormSet()
        context['contact_formset_helper'] = ContactFormSetHelper()
        return context

    def form_valid(self, form):
        dataset = form.save()
        invalid_form = False

        new_contact_form = NewContactForm(self.request.POST)
        contact_form = ContactForm(self.request.POST)
        if new_contact_form.is_valid() and new_contact_form.has_changed():
            new_contact = new_contact_form.save()
            new_contact.save()
            dataset.contact = new_contact
        elif contact_form.is_valid():
            dataset.contact = contact_form.cleaned_data['contact']
        elif not(new_contact_form.is_valid() or contact_form.is_valid()):
            invalid_form = True

        investigator_formset = InvestigatorFormSet(self.request.POST,
            self.request.FILES, instance=dataset)
        if investigator_formset.is_valid():
            investigator_formset.save()
        else:
            invalid_form = True

        link_formset = LinkFormSet(self.request.POST, instance=dataset)
        if link_formset.is_valid():
            link_formset.save()
        else:
            invalid_form = True

        publication_document_formset = PublicationDocumentFormSet(
            self.request.POST, self.request.FILES, instance=dataset)
        if publication_document_formset.is_valid():
            publication_document_formset.save()
        else:
            invalid_form = True

        publication_pubmed_link_formset = PublicationPubMedLinkFormSet(
            self.request.POST, instance=dataset)
        if publication_pubmed_link_formset.is_valid():
            publication_pubmed_link_formset.save()
        else:
            invalid_form = True

        revision_formset = RevisionFormSet(self.request.POST, 
            instance=dataset)
        if revision_formset.is_valid():
            revision_formset.save()
        else:
            invalid_form = True
        
        task_formset = TaskFormSet(self.request.POST, self.request.FILES,
            instance=dataset)
        if task_formset.is_valid():
            task_formset.save()
        else:
            invalid_form = True
        
        if invalid_form:
            context = {
                'request': self.request,
                'form': form,
                'new_contact_form': new_contact_form,
                'contact_form': contact_form,
                'investigator_formset': investigator_formset,
                'link_formset': link_formset,
                'publication_document_formset': publication_document_formset,
                'publication_pubmed_link_formset': publication_pubmed_link_formset,
                'revision_formset': revision_formset,
                'task_formset': task_formset,
                'investigator_formset_helper': InvestigatorFormSetHelper(),
                'link_formset_helper': LinkFormSetHelper(),
                'publication_document_formset_helper': PublicationDocumentFormSetHelper(),
                'publication_pubmed_link_formset_helper': PublicationPubMedLinkFormSetHelper(),
                'task_formset_helper': TaskFormSetHelper(),
                'revision_formset_helper': RevisionFormSetHelper()
            }
            return self.render_to_response(context)
        else:
            return super(DatasetCreateUpdate, self).form_valid(form)



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

    def form_valid(self, form):
        user_request = form.save()
        dataset = Dataset()
        dataset.project_name = "Request for " + user_request.user_email_address
        dataset.save()
        user_request.dataset = dataset
        user_request.save()
        return super(UserDataRequestCreate, self).form_valid(form)

class UserDataset(SingleObjectTemplateResponseMixin, ModelFormMixin,
                  ProcessFormView):
    model = Dataset
    form_class = UserDatasetForm
    success_url = reverse_lazy('dataset_list')
    template_name = "dataset/user_dataset_form.html"
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(UserDataset, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(UserDataset, self).post(request, *args, **kwargs)

    def get_object(self):
        token = self.kwargs.get('token') 
        user_data_request = get_object_or_404(UserDataRequest, token=token)
        return user_data_request.dataset

    ''' alternative method of binding dataset to user data request
    def form_valid(self, form):
        dataset = form.save()
        token = self.kwargs.get('token') 
        user_data_request = get_object_or_404(UserDataRequest, token=token)
        if user_data_request.dataset == None:
            user_data_request.dataset = dataset
            user_data_request.save()
        return super(UserDataset, self).form_valid(form)
    '''
        

class UserDatasetCreate(CreateView):
    model = Dataset
    form_class = UserDatasetForm
    success_url = reverse_lazy('dataset_list')
    template_name = "dataset/user_dataset_form.html"

    # Check to make sure the token exists, if not 404
    def dispatch(self, *args, **kwargs):
        token = self.kwargs.get('token') 
        user_data_request = get_object_or_404(UserDataRequest, token=token)
        return super(UserDatasetCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        dataset = form.save()
        token = self.kwargs.get('token') 
        user_data_request = get_object_or_404(UserDataRequest, token=token)
        user_data_request.save()
        return super(UserDatasetCreate, self).form_valid(form)
        

class Index(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['num_datasets'] = len(Dataset.objects.filter(status='PUBLISHED'))
        total = 0
        for x in Dataset.objects.filter(status='PUBLISHED'):
            if x.sample_size is not None:
                total += x.sample_size
        context['num_subjects'] =  total
        return context

class ReferencePaperList(LoginRequiredMixin, ListView):
    model = ReferencePaper

class ReferencePaperDelete(LoginRequiredMixin, DeleteView):
    model = ReferencePaper
    success_url = reverse_lazy('reference_paper_list')

class ReferencePaperCreate(LoginRequiredMixin, CreateView):
    model = ReferencePaper
    form_class = ReferencePaperForm
    success_url = reverse_lazy('reference_paper_list')

class ReferencePaperUpdate(LoginRequiredMixin, UpdateView):
    model = ReferencePaper
    form_class = ReferencePaperForm
    success_url = reverse_lazy('reference_paper_list')

