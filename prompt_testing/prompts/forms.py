from django import forms
from .models import Prompt  # Assuming Prompt model is in the same app

class PromptForm(forms.ModelForm):
    class Meta:
        model = Prompt
        fields = ['text']  # Specify model fields to include in the form
