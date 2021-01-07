from django import forms
from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['content'].label = False
        self.fields['content'].widget.attrs.update({'autofocus': 'autofocus', 'placeholder': 'Send a message!'})
