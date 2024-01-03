from django import forms
from .models import Bid, Job

class BidForm(forms.ModelForm):
    """Bid Form"""
    class Meta:
        model = Bid
        fields = ['bid_amount', 'project_duration', 'proposal', 'candidate_reason']
        
class JobForm(forms.ModelForm):
    """Job form"""
    class Meta:
        model = Job
        fields = "__all__"

