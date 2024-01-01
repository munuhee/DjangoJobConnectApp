from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.db.models import Avg
from ckeditor_uploader.fields import RichTextUploadingField
from autoslug import AutoSlugField

class Category(models.Model):
    """Model representing a category for posts."""
    name = models.CharField(max_length=50, help_text='Enter a category name')

    def __str__(self):
        return self.name

class Post(models.Model):
    """Model representing a blog post."""
    title = models.CharField(max_length=100)
    short_description = models.CharField(max_length=150, blank=True, null=True)
    main_description = RichTextUploadingField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    slug = AutoSlugField(unique=True, populate_from='title')
    last_rating = models.IntegerField(default=0)
    categories = models.ManyToManyField(Category, help_text='Select categories for this post')

    class Meta:
        verbose_name_plural = "All projects"
        ordering = ["date_posted"]

    def __str__(self):
        return f'{self.title} by {self.author} ({self.slug})'

    def get_absolute_url(self):
        """Returns the absolute URL to access a detail record for this post."""
        return reverse('post-detail', kwargs={'slug': self.slug})

    @property
    def actual_rating(self):
        """Generates a list representing the actual rating in stars."""
        return list(range(self.last_rating))

    @property
    def calc_rating(self):
        """Calculates and returns the average rating of the post."""
        average_rating = PostReview.objects.filter(post=self).aggregate(Avg('rating'))
        return average_rating['rating__avg'] if average_rating['rating__avg'] else 0

    def save(self, *args, **kwargs):
        """Overrides save method to auto-generate slug."""
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

class PostReview(models.Model):
    """Model representing a review for a post."""
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='reviews', help_text='Select a post to review')
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]  # Rating scale from 1 to 5
    rating = models.IntegerField(choices=RATING_CHOICES, help_text='Select a rating')

class PostComment(models.Model):
    """Model representing a comment on a post."""
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments', help_text='Select a post to comment on')
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    text = models.CharField(max_length=300, help_text='Enter your comment')

class Contact(models.Model):
    """Model representing a contact form entry."""
    name = models.CharField(max_length=100, help_text='Enter your name')
    email = models.EmailField(max_length=100, help_text='Enter your email')
    message = models.TextField(max_length=100, help_text='Enter your message')
    date_contacted = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        """Returns the absolute URL after a contact form entry is created."""
        return reverse('home')
