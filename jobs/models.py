from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from notifications.signals import notify
from django.utils.text import Truncator


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Requirement(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Job(models.Model):
    JOB_STATUS = (
        ("Open", "Open"),
        ("Closed", "Closed"),
    )
    company_name = models.CharField(max_length=200, blank=False, null=False)
    job_title = models.CharField(max_length=200, blank=True, null=True)
    job_description = models.TextField(blank=False)
    pub_date = models.DateTimeField(default=timezone.now)
    budget = models.CharField(max_length=20, help_text="eg, 15-35 USD",null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    requirements = models.ManyToManyField(Requirement)

    def __str__(self):
        return self.job_title

    def get_absolute_url(self):
        return reverse('job_detail', args=[self.pk])



class Application(models.Model):
    job = models.ForeignKey(Job, related_name='applications', on_delete=models.CASCADE)
    content = models.TextField(blank=False)
    budget = models.CharField(max_length=25, help_text="eg, 30 USD in 30 days",null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse('job_detail', kwargs={'pk': self.job.pk})  # returns a string to the job detail that uses the pk of the comment instance. job. pk to link to the correct detail page ie. /job/

    def save(self, *args, **kwargs):
        super(Application, self).save(*args, **kwargs)
        n = 4
        truncatewords = Truncator(self.content).words(n)
        notify.send(self.author, recipient=self.job.author, verb='commented "' + truncatewords + '" on your post!', action_object=self.job, description='comment', target=self)