import requests
import smtplib

from django import forms
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.forms import Form, ModelForm
from django.forms.models import inlineformset_factory
from django.forms.widgets import TextInput
from django.template.loader import render_to_string
from django.utils.crypto import salted_hmac

from ckeditor.widgets import CKEditorWidget

from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Column, Field, Fieldset, \
    Layout, Row, Submit

from dataset.models import Contact, Dataset, FeaturedDataset, Investigator, \
    Link, PublicationPubMedLink, PublicationDocument, Revision, Task, \
    UserDataRequest

class ContactForm(Form):
    contact = forms.ModelChoiceField(queryset=Contact.objects.all().order_by('name'))

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "Existing Contacts",
                Field('contact', css_class="form-control"),
                css_class="fieldset-control form-control"
            )
        )
        self.helper.form_tag = False

class NewContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = [
            'name', 'email', 'website'
        ]

        widgets = {
            'website': TextInput(),
        }
        
    def __init__(self, *args, **kwargs):
        super(NewContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "New Contact Information",
                Field('name', css_class="form-control"),
                Field('email', css_class="form-control"),
                Field('website', css_class="form-control"),
                css_class="fieldset-control form-control"
            ),
        )
        self.helper.form_tag = False

class DatasetForm(ModelForm):
    class Meta:
        model = Dataset
        fields = [
            'workflow_stage', 'status', 'project_name', 'summary', 
            'sample_size', 'scanner_type', 'accession_number', 
            'acknowledgements', 'license_title', 'license_url', 'curated' 
        ]
        
        widgets = {
            'license_url': TextInput(),
            'aws_link_url': TextInput(),
            'summary': CKEditorWidget()
        }
    
    def __init__(self, *args, **kwargs):
        super(DatasetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('workflow_stage', css_class="form-control"),
            Field('status', css_class="form-control"),
            Field('curated', css_class="form-control"),
            Field('project_name', css_class="form-control"),
            Field('summary', css_class="form-control", rows=3),
            Field('sample_size', css_class="form-control"),
            Field('scanner_type', css_class="form-control", rows=1),
            Field('accession_number', css_class="form-control"),
            Field('acknowledgements', css_class="form-control", rows=3),
            Field('license_title', css_class="form-control"),
            Field('license_url', css_class="form-control"),
        )
        self.helper.form_tag = False

class UserDatasetForm(ModelForm):
    '''
    A Subset of the normal dataset form. This is the form that will be exposed
    to people wishing to upload data to the site.
    '''
    class Meta:
        model = Dataset
        fields = [
            'project_name', 'summary', 'sample_size', 'scanner_type', 
            'acknowledgements'
        ]
        widgets = {
            'summary': CKEditorWidget(),
        }
    
    def __init__(self, *args, **kwargs):
        super(UserDatasetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('project_name', css_class="form-control"),
            Field('summary', css_class="form-control", rows=3),
            Field('sample_size', css_class="form-control"),
            Field('scanner_type', css_class="form-control", rows=1),
            Field('acknowledgements', css_class="form-control", rows=3),
        )
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

class InvestigatorForm(ModelForm):
    class Meta:
        model = Investigator
        fields = ['investigator']

class LinkForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(LinkForm, self).__init__(*args, **kwargs)
        dataset = self.instance.dataset_id
        queryset = Revision.objects.filter(dataset_id=dataset)
        self.fields['revision'].queryset = queryset
    class Meta:
        model = Link
        fields = ['title', 'url', 'revision']
        widgets = {
            'url': TextInput()
        }

class PublicationDocumentForm(ModelForm):
    class Meta:
        model = PublicationDocument
        fields = ['document']

class PublicationPubMedLinkForm(ModelForm):
    class Meta:
        model = PublicationPubMedLink
        fields = ['title', 'url']

        widgets = {
            'url': TextInput()
        }

class RevisionForm(ModelForm):
    class Meta:
        model = Revision
        fields = ['revision_number', 'notes']
        widgets = {
            'aws_link_url': TextInput()
        }

class TaskForm(ModelForm):
    cogat_id = forms.ChoiceField()

    class Meta:
        model = Task
        fields = ['cogat_id', 'number']

    def get_cogat_tasks(self):
        cogat_tasks = requests.get('http://cognitiveatlas.org/api/v-alpha/task')
        tasks_json = cogat_tasks.json()
        tasks_choices = [("", "---------")]
        for elem in tasks_json:
            tasks_choices.append((elem['id'], elem['name']))
        
        return tasks_choices

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['cogat_id'].choices = self.get_cogat_tasks()

InvestigatorFormSet = inlineformset_factory(
    Dataset, Investigator, form=InvestigatorForm, extra=1, can_delete=True)

LinkFormSet = inlineformset_factory(
    Dataset, Link, form=LinkForm, extra=1, can_delete=True)

PublicationDocumentFormSet = inlineformset_factory(
    Dataset, PublicationDocument, form=PublicationDocumentForm, extra=1, 
    can_delete=True)

PublicationPubMedLinkFormSet = inlineformset_factory(
    Dataset, PublicationPubMedLink, form=PublicationPubMedLinkForm, extra=1, 
    can_delete=True)
    
RevisionFormSet = inlineformset_factory(
    Dataset, Revision, form=RevisionForm, extra=1, can_delete=True)

TaskFormSet = inlineformset_factory(
    Dataset, Task, form=TaskForm, extra=1, can_delete=True)

class InvestigatorFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(InvestigatorFormSetHelper, self).__init__(*args, **kwargs)
        self.layout = Layout(
            Fieldset(
                "",
                Field('investigator', css_class="form-control"),
                Field('DELETE', css_class='form-control'),
                css_class="fieldset-control form-control"
            )
        )
        self.form_tag = False

class LinkFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(LinkFormSetHelper, self).__init__(*args, **kwargs)
        self.layout = Layout(
            Fieldset(
                "Link",
                Field('title', css_class="form-control"),
                Field('url', css_class="form-control"),
                Field('revision', css_class="form-control"),
                Field('DELETE', css_class="form-control"),
                css_class="fieldset-control form-control"
            )
        )
        self.form_tag = False

class PublicationDocumentFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(PublicationDocumentFormSetHelper, self).__init__(*args, **kwargs)
        self.layout = Layout(
            Fieldset(
                "Publication Document",
                Field('document', css_class="form-control"),
                Field('DELETE', css_class='form-control'),
                css_class="fieldset-control form-control"
            )
        )
        self.form_tag = False

class PublicationPubMedLinkFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(PublicationPubMedLinkFormSetHelper, self).__init__(*args, 
            **kwargs)
        self.layout = Layout(
            Fieldset(
                "PubMed Link",
                Field('title', css_class="form-control"),
                Field('url', css_class="form-control"),
                Field('DELETE', css_class='form-control'),
                css_class="fieldset-control form-control"
            )
        )
        self.form_tag = False

class RevisionFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(RevisionFormSetHelper, self).__init__(*args, **kwargs)
        self.layout = Layout(
            Fieldset(
                "Revision Information",
                Field('revision_number', css_class="form-control"),
                Field('notes', css_class="form-control", rows=3),
                Field('DELETE', css_class='form-control'),
                css_class="fieldset-control form-control"
            ),
        )
        self.form_tag = False

class TaskFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(TaskFormSetHelper, self).__init__(*args, **kwargs)
        self.layout = Layout(
            Fieldset(
                "Cognitive Atlas Task",
                Field('cogat_id', css_class="form-control"),
                Field('number', css_class="form-control"),
                Field('DELETE', css_class='form-control'),
                css_class="fieldset-control form-control task_set"
            ),
        )
        self.form_tag = False

class FeaturedDatasetForm(ModelForm):
    class Meta:
        model = FeaturedDataset
        fields = ['dataset', 'image', 'title', 'content']
    
    def __init__(self, *args, **kwargs):
        super(FeaturedDatasetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('dataset', css_class="form-control"),
            Field('title', css_class="form-control"),
            Field('image', css_class="form-control"),
            Field('content', css_class="form-control"),
        )
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Add Featured Dataset'))

'''
    This form is used to send out links to views containing UserDatasetForms. 
    Provided the email address passess validation a message containing a 
    hased link will be sent in the overridden save function. Using the 
    date field for salt allows for multiple forms with unique urls to be sent
    to the same email address.
'''
class UserDataRequestForm(ModelForm):
    class Meta:
        model = UserDataRequest
        fields = ['user_email_address']
        
    def __init__(self, *args, **kwargs):
        super(UserDataRequestForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('user_email_address', css_class="form-control")
        )
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Send Request for Information'))
    
    def save(self, fail_silently=False):
        try:
            data_request = super(UserDataRequestForm, self).save()
            data_request.token = salted_hmac(data_request.request_sent, 
                                             data_request.user_email_address).hexdigest()
            data_request.save()
            subject = "Request for data from OpenfMRI.org"
            body = render_to_string(
                "dataset/user_data_request_email_body.txt", 
                {'url': reverse('user_dataset',
                                args=[data_request.token])}
            )
            send_mail(subject, body, 'openfmri@gmail.com', 
                      [data_request.user_email_address], fail_silently)
            return data_request
        except smtplib.SMTPException:
            raise smtplib.SMTPException
            
