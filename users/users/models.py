from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from ckeditor.fields import RichTextField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verify = models.BooleanField(default=False)
    profile_picture = ProcessedImageField(default='profile_pics/default.jpg', upload_to='profile_pics', format='JPEG',
                                processors = [ResizeToFill(150,150)],
                                options={ 'quality': 100})
    telephone = PhoneNumberField(null=True,blank=True)
    email = models.CharField(max_length=150, blank=True, null=True)
    bio = models.CharField(max_length=150, blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    country = CountryField(blank_label='(select country)', blank=True, null=True)
    curriculum_vitae  = RichTextField()
    followers = models.ManyToManyField(User, blank=True, related_name='user_followers')
    
    def get_number_of_followers(self):
        print(self.followers.count())
        if self.followers.count():
            return self.followers.count()
        else:
            return 0

    def get_number_of_following(self):
        if self.following.count():
            return self.following.count()
        else:
            return 0
        
    def __str__(self):
        return f'{self.user.username} Profile'

