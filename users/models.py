from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

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
    bio = models.TextField()
    profile_image = models.ImageField(upload_to='profile_images/', default="profile_images/default.jpg")
    job_status = models.CharField(max_length=20, choices=JOB_CHOICES, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        """
        Override the save method to
        define the image aspect ratio
        """
        if self.profile_image:
            img = Image.open(self.profile_image)
            output = BytesIO()

            # Define the aspect ratio (1:1)
            target_width = target_height = 300

            img.thumbnail((target_width, target_height))

            # Save the resized image to the BytesIO object
            img.save(output, format='JPEG', quality=75)
            output.seek(0)

            # Set the image content to the associated ImageField
            self.profile_image.file = ContentFile(output.getvalue())

        super().save(*args, **kwargs)

    def __str__(self):
        """String representation of the profile."""
        return f"Profile of {self.user.username}"

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

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
