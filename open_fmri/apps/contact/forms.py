from contact_form.forms import ContactForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Field, Layout, Submit

class CrispyContactForm(ContactForm):
    def __init__(self, *args, **kwargs):
        super(CrispyContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('name', css_class="form-control"),
            Field('email', css_class="form-control"),
            Field('body', css_class="form-control"),
        )
        self.helper.form_method = 'post'
        self.helper.field_class = 'form-control'
        self.helper.add_input(Submit('submit', 'Send Message'))
