from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
import json
from django.urls import  reverse
from .models import *
from memberships.models import *
from memberships.views import *
from .forms import *
from .decorators import *
from django.contrib.auth.models import User
from django.views.generic.edit import FormMixin
from django.db.models import Count
from django.contrib import messages
from users.models import Profile
from django.forms import modelformset_factory
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
import operator
from django.core import serializers
from functools import reduce
from django.db.models import Q
# Create your views here.


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'core/projects.html'
    ordering = ['-last_rating']
    paginate_by = 6

class UserPostListView(ListView):
    model = Post
    template_name = 'core/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(FormMixin, DetailView):
    model = Post
    form_class = CommentForm

    def get_success_url(self):
        return reverse('post-detail', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['comments'] = PostComment.objects.filter(
            post=self.object).order_by('-id')
        return context


    def form_valid(self, form):
        p = self.get_object()
        text = form.cleaned_data['text']
        new_comment = PostComment(text=text, post=p, user=self.request.user)
        new_comment.save()
        messages.success(self.request, "Your comment is added, thank you")
        return super().form_valid(form)

#@userplan_required(plan_types=["Standard","Unlimited"])
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['cover_image','title','overview','description', 'category']


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


    def post(self, request, *args, **kwargs):
        if request.user.userplan.plan.plan_type == "Unlimited"  or request.user.is_superuser or request.user.userplan.plan.plan_type == "Standard":
            if not request.user.is_authenticated:
                return HttpResponseForbidden()
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        else:
            return HttpResponseRedirect(reverse('plan'))


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['cover_image','title','overview','description','category']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False




def category(request, link):
    categories = {
        "graphics-design": "Graphics & Design",
        "Photography": "Photography",
        "Photoshop": "Photoshop",
        "Architecture Services": "Architecture Services",
        "Marketing, Sales and Service":"Marketing, Sales and Service",
        "Data Entry": "Data Entry",
        "Web Development and Designing" : "Web Development and Designing",
        "Teaching and Tutoring" : "Teaching and Tutoring",
        "Creative Design" : "Creative Design",
        "Mobile App Development" : "Mobile App Development",
        "3D Modeling and CAD" : "3D Modeling and CAD",
        "Game Development" : "Game Development",
        "Translation" : "Translation",
        "Transcription" : "Transcription",
        "Article and Blog Writing" : "Article and Blog Writing",
        "Logo Design and illustration" : "Logo Design and illustration",
        "Audio and Video Production" : "Audio and Video Production",
    }
    try:
        posts = Post.objects.filter(category=categories[link])
        return render(request, 'core/projects.html', {"posts": posts})
    except KeyError:
        return redirect('home')


def search(request):
    context = {
        'posts': Post.objects.filter(title__contains=request.GET['title'])
    }

    return render(request, 'core/post_search_results.html', context)


@login_required
def public_profile(request, username):
    obj = User.objects.get(username=username)  # grabs <username> from url and stores it in obj to  be passed into the context
    context = {
        'posts': Post.objects.filter(author__username=obj).order_by('-date_posted'),
        'username': obj,  # obj is now accesible in the html via the variable {{ username }}

    }
    return render(request, 'core/public_profile.html', context)

@login_required(login_url='login')
def rate_post_view(request, slug, rating):
    try:
        p = Post.objects.get(slug=slug)
        if p and not(PostReview.objects.filter(user=request.user).filter(post=p)):
            review = PostReview(post=p, user=request.user, rating=rating)
            review.save()
            p.last_rating = p.calc_rating
            p.save()
            messages.success(
                request, f'You rated a post: {p.title}')

        else:
            messages.warning(
                request, f'You already rated this post')
        return redirect('post-detail', slug=p.slug)
    except Post.DoesNotExist:
        raise Http404("Post is unavailable")
    return redirect('post-detail', slug=p.slug)

@login_required(login_url='login')
def comment(request, slug):
    return redirect('post-detail', slug=slug)



class ContactCreateView(CreateView):
    model = Contact
    fields = ['name','email', 'message']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostSearchListView(PostListView):
    """
    Display a Blog List page filtered by the search query.
    """
    paginate_by = 6

    def get_queryset(self):
        result = super(PostSearchListView, self).get_queryset()

        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(title__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(overview__icontains=q) for q in query_list))
            )

        return result