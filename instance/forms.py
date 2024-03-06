from django import forms

from question.models import Category, Question, Option
from .models import Instance
from docx import Document


class CreateInstanceForm(forms.ModelForm):
    title = forms.CharField()
    description = forms.Textarea()

    class Meta:
        model = Instance
        fields = ['title', 'description']
