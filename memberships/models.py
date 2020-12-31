from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from users.models import *
from django.utils import timezone
#from countdowntimer_model.models import CountdownTimer
        
        
# Create your models here.  


SUB_PLANS = (
        ("Basic", "Basic"),
        ("Standard", "Standard"),  
        ("Unlimited", "Unlimited"), 
    )  

class Plan(models.Model):
    plan_type = models.CharField(max_length=15, choices=SUB_PLANS, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    attributes = RichTextUploadingField(null=True, blank=True)
    
    def __str__(self):
        return self.plan_type
 
 
class UserPlan(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True, blank=True)
    date_subscribed = models.DateTimeField(default=timezone.now)
    #userplan_timer = CountdownTimer(duration_in_minutes=123,state=CountdownTimer.STATE.RUNNING)
   
