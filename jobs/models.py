"""
Module containing Django models for job-related functionality.

This module defines the following Django models:
- Category: Represents a job category.
- Requirement: Represents a job requirement.
- Job: Represents a job post.
- Application: Represents a job application.

Each model has specific fields and methods related to job management.
"""
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

    name = models.CharField(max_length=200)

    def __str__(self):
        """Return the string representation of the category."""
        return self.name


class Requirement(models.Model):
    """A model representing a job requirement."""

    name = models.CharField(max_length=200)

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
class Bid(models.Model):
    """A model representing a bid."""
    job = models.ForeignKey('jobs.Job', on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    project_duration = models.IntegerField()
    proposal = models.TextField()
    candidate_reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the string representation of the bid."""
        return f"Bid by {self.bidder.username} for {self.job.job_title}"
