from django.contrib import admin
from . models import *
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fields = ('title', 'overview', 'author', 'description', 'date_posted',
              'category','cover_image')

    list_display = ('title', 'author', 'category', 'slug', 'date_posted')
    search_fields = ['title']
    
admin.site.register(PostComment)

@admin.register(Contact)
class Contact(admin.ModelAdmin):

    list_display = ('name', 'email', 'date_contacted', 'message')
    
'''
@admin.register(OrderItem)
class PostAdmin(admin.ModelAdmin):

    list_display = ('post', 'order', 'quantity', 'date_added')

admin.site.register(PostFile)
'''