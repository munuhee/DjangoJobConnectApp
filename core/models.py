from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from PIL import Image
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
    description = RichTextUploadingField(null=False,blank=False)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='author')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="O")
    slug = AutoSlugField(unique=True, populate_from='title')
    last_rating = models.IntegerField(default=0)
    cover_image = models.ImageField(upload_to='post_pics', height_field=300, width_field=300, max_length=100)
    
    class Meta:
        verbose_name_plural = "All projects"
        ordering = ["date_posted"]
    
    def save(self, *args, **kwargs):
        try:
            img = Image.open(self.cover_image)
            if img.width > 1000 or img.height > 1000:
                raise ValidationError("Image size must be no larger than 1000x1000")
        except:
            raise ValidationError("The image file is invalid")
        super().save(*args, **kwargs)   
      
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
'''
class Order(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return str(self.id)
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total(self):
        total = self.post.price * self.quantity
        return total
'''
class Contact(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    email = models.CharField(max_length=100, blank=False, null=False)
    message = models.TextField(max_length=100, blank=False, null=False)
    date_contacted = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('home')
    