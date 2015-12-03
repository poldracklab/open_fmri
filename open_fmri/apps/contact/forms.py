import smtplib

from django.core.mail import send_mail

from contact_form.forms import ContactForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Field, Layout, Submit

class CrispyContactForm(ContactForm):
    def __init__(self, *args, **kwargs):
        super(CrispyContactForm, self).__init__(*args, **kwargs)
        self.fields['body'].label = "Describe Your Dataset"
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('name', css_class="form-control"),
            Field('email', css_class="form-control"),
            Field('body', css_class="form-control"),
        )
        self.helper.form_method = 'post'
        self.helper.field_class = 'form-control'
        self.helper.add_input(Submit('submit', 'Send Message'))

    def save(self):
        contact_form = super(CrispyContactForm, self).save() 
        try:
            subject = "Information About Your Dataset Has Been Recieved"
            body = "A Data Curator will be in contact with you shortly. "
            send_mail(subject, body, 'admin@openfmri.org', 
                      [self.cleaned_data['email']])
            return contact_form
        except smtplib.SMTPException:
            raise smtplib.SMTPException
        super(CrispyContactForm, self).save()
