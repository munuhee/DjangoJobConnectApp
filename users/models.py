from django.db import models
from django.contrib.auth.models import User

from django.conf import settings
from django.db import models

class Profile(models.Model):
    JOB_CHOICES = [
        ('open', 'Open to Work'),
        ('employed', 'Employed'),
        ('student', 'Student'),
        ('freelance', 'Freelance'),
        ('unemployed', 'Unemployed'),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', default="profile_images/default.jpg")
    job_status = models.CharField(max_length=20, choices=JOB_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.user.username
class Experience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

class Education(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    degree = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

class Contact(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    address = models.CharField(max_length=100,null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
