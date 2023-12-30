from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Profile(models.Model):
    """Model representing a user profile."""
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
        """String representation of the profile."""
        return f"Profile of {self.user.username}"

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

class Experience(models.Model):
    """Model representing work experience."""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        """String representation of the experience."""
        return f"{self.title} at {self.company}"

    class Meta:
        verbose_name = 'Experience'
        verbose_name_plural = 'Experiences'
        ordering = ['-start_date']

class Education(models.Model):
    """Model representing education details."""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    degree = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        """String representation of the education."""
        return f"{self.degree} at {self.institution}"

    class Meta:
        verbose_name = 'Education'
        verbose_name_plural = 'Educations'
        ordering = ['-start_date']

class Contact(models.Model):
    """Model representing contact information."""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    address = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)

    def __str__(self):
        """String representation of the contact."""
        return f"Contact for {self.profile.user.username}"

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
