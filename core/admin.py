from django.contrib import admin
from .models import Topic, Post, PostReview, PostComment, Contact

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_posted', 'last_rating', 'calc_rating')

@admin.register(PostReview)
class PostReviewAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'rating')

@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'text')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'date_contacted')
