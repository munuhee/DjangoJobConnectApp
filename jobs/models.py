from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.utils.text import Truncator

from ckeditor_uploader.fields import RichTextUploadingField
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from notifications.signals import notify


class Category(models.Model):
    """A model representing a job category."""

    name = models.CharField(max_length=50)

    def __str__(self):
        """Return the string representation of the category."""
        return self.name


class Requirement(models.Model):
    """A model representing a job requirement."""

    name = models.CharField(max_length=50)

    def __str__(self):
        """Return the string representation of the requirement."""
        return self.name


class Job(models.Model):
    """A model representing a job post."""

    JOB_STATUS = (
        ("Open", "Open"),
        ("Closed", "Closed"),
    )
    company_name = models.CharField(max_length=200, blank=False, null=False)
    job_title = models.CharField(max_length=200, blank=True, null=True)
    job_description = models.TextField(blank=False)
    pub_date = models.DateTimeField(default=timezone.now)
    budget = models.CharField(max_length=100, help_text="eg, 15-35 USD", null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    requirements = models.ManyToManyField(Requirement)

    def __str__(self):
        """Return the string representation of the job."""
        return self.job_title

    def get_absolute_url(self):
        """Get the absolute URL for a job detail view."""
        return reverse('job_detail', args=[self.pk])


class Application(models.Model):
    """A model representing a job application."""

    job = models.ForeignKey(Job, related_name='applications', on_delete=models.CASCADE)
    content = models.TextField(blank=False)
    budget = models.CharField(max_length=25, help_text="eg, 30 USD in 30 days", null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        """Return the string representation of the application content."""
        return self.content

    def get_absolute_url(self):
        """Get the absolute URL for an application."""
        return reverse('job_detail', kwargs={'pk': self.job.pk})

    def save(self, *args, **kwargs):
        """Override save method to trigger notifications."""
        super(Application, self).save(*args, **kwargs)
        n = 4
        truncatewords = Truncator(self.content).words(n)
        notify.send(
            self.author,
            recipient=self.job.author,
            verb='commented "' + truncatewords + '" on your post!',
            action_object=self.job,
            description='comment',
            target=self
        )
