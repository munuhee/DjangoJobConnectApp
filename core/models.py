from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from PIL import Image
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from autoslug import AutoSlugField
from users.models import Profile
from memberships.models import *

class Post(models.Model):
    CATEGORY_CHOICES = (
        ("graphics-design", "Graphics & Design"),
        ("Photography", "Photography"),
        ("Photoshop", "Photoshop"),
        ("Architecture Services", "Architecture Services"),
        ("Marketing, Sales and Service","Marketing, Sales and Service"),
        ("Data Entry", "Data Entry"),
        ("Web Development and Designing", "Web Development and Designing"),
        ("Teaching and Tutoring", "Teaching and Tutoring"),
        ("Creative Design", "Creative Design"),
        ("Mobile App Development", "Mobile App Development"),
        ("3D Modeling and CAD", "3D Modeling and CAD"),
        ("Game Development", "Game Development"),
        ("Translation", "Translation"),
        ("Transcription", "Transcription"),
        ("Article and Blog Writing", "Article and Blog Writing"),
        ("Logo Design and illustration", "Logo Design and illustration"),
        ("Audio and Video Production", "Audio and Video Production"),
    )

    title = models.CharField(max_length=100)
    overview = models.CharField(max_length=100,default='explore to find more about my capabilities')
    description = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='author')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="O")
    slug = AutoSlugField(unique=True, populate_from='title')
    last_rating = models.IntegerField(default=0)
    image = ProcessedImageField(upload_to='project_pics', format='JPEG', processors = [ResizeToFill(360,200)],
                options={ 'quality': 100})
    class Meta:
        verbose_name_plural = "All projects"
        ordering = ["date_posted"]

    def __str__(self):
        return '%s' ' ' 'by' ' ' '%s'  ' ' '(%s)'  %(self.title,self.author, self.slug)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.slug})

    @property
    def actual_rating(self):
        list_of_stars = []
        for star in range(self.last_rating):
            list_of_stars.append(star)
        return list_of_stars

    @property
    def calc_rating(self):
        ratings = PostReview.objects.filter(post=self)
        if ratings:
            result = 0
            for rating in ratings:
                result += rating.rating
            result = int(result / len(ratings))
            return result
        else:
            return 0

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

class PostReview(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    rating = models.IntegerField()


class PostComment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    text = models.CharField(max_length=300)

class Contact(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    email = models.CharField(max_length=100, blank=False, null=False)
    message = models.TextField(max_length=100, blank=False, null=False)
    date_contacted = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('home')
