from django import forms
from documents.models import Document


# Form to handling scraping a new document
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('name', 'url', 'tags',)
