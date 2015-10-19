
from django.conf.urls import url
from django.views.generic import TemplateView

from contact.views import CrispyContactFormView


urlpatterns = [
    url(r'^$',
        CrispyContactFormView.as_view(),
        name='contact_form'),
    url(r'^sent/$',
        TemplateView.as_view(
            template_name='contact_form/contact_form_sent.html'),
        name='contact_form_sent'),
]
