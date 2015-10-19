from django.shortcuts import render

from contact_form.views import ContactFormView

from .forms import CrispyContactForm

class CrispyContactFormView(ContactFormView):
    form_class = CrispyContactForm
