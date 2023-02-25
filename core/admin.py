from django.contrib import admin
from .models import Post, Contact, Category

class PostAdmin(admin.ModelAdmin):
    fields = ('title', 'overview', 'author', 'description', 'date_posted',
              'category', 'image')
    list_display = ('title', 'author', 'slug', 'date_posted')
    search_fields = ['title']
admin.site.register(Post, PostAdmin)

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'date_contacted', 'message')
admin.site.register(Contact, ContactAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Category, CategoryAdmin)
