from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Topic, Post, PostReview, PostComment, Contact

class TopicForm(forms.ModelForm):
    """Form for creating or updating a Topic instance."""
    class Meta:
        model = Topic
        fields = ['name']

class PostForm(forms.ModelForm):
    """Form for creating or updating a Post instance."""
    main_description = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Post
        fields = ['title', 'short_description', 'main_content', 'topics']

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
