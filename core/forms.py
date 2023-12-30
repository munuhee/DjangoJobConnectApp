from django import forms
from .models import Category, Post, PostReview, PostComment, Contact

class CategoryForm(forms.ModelForm):
    """Form for creating or updating a Category instance."""
    class Meta:
        model = Category
        fields = ['name']

class PostForm(forms.ModelForm):
    """Form for creating or updating a Post instance."""
    class Meta:
        model = Post
        fields = ['title', 'overview', 'description', 'image', 'categories']

class ReviewForm(forms.ModelForm):
    """Form for creating or updating a PostReview instance."""
    class Meta:
        model = PostReview
        fields = ['post', 'user', 'rating']

class CommentForm(forms.ModelForm):
    """Form for creating or updating a Comment instance."""
    class Meta:
        model = PostComment
        fields = ['post', 'user', 'text']

class ContactForm(forms.ModelForm):
    """Form for creating or updating a Contact instance."""
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
