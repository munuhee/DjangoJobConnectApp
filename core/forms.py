from django import forms
from django.forms import inlineformset_factory
from .models import *

class CommentForm(forms.Form):
    text = forms.CharField(label='Add comment:', widget=forms.Textarea(
        attrs={'rows': 4, 'cols': 15}))

