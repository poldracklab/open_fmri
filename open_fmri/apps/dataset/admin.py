from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget

from django.contrib.flatpages.models import FlatPage

class FlatPageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FlatPageForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget = CKEditorWidget()

class FlatPageAdmin(admin.ModelAdmin):
    form = FlatPageForm

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
