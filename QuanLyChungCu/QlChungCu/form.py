from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from QlChungCu.models import *


class LettersForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Letters
        fields = '__all__'
