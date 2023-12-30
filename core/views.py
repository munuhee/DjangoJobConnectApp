from django.shortcuts import render, get_object_or_404, redirect
from django.http import (
    HttpResponseRedirect, HttpResponseForbidden, JsonResponse, Http404
)
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
from functools import reduce
import operator
from subscription.models import UserSubscription
from .models import Post, PostComment, PostReview, Contact
from .forms import CommentForm, PostForm, ContactForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
import datetime

def post_list(request):
    """
    View for listing all posts.

    Retrieves all posts and renders them in the 'projects.html' template.

    Args:
    - request: HTTP request object.

    Returns:
    - Rendered response displaying all posts.
    """
    posts = Post.objects.order_by('-last_rating')
    context = {'posts': posts}
    return render(request, 'core/projects.html', context)


def user_post_list(request, username):
    """
    View for listing posts by a specific user.

    Retrieves posts by a specific user and renders them in the 'user_posts.html' template.

    Args:
    - request: HTTP request object.
    - username: Username of the user whose posts are being fetched.

    Returns:
    - Rendered response displaying posts by the specified user.
    """
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user).order_by('-date_posted')
    context = {'posts': posts}
    return render(request, 'core/user_posts.html', context)


def post_detail(request, slug):
    """
    View for displaying details of a specific post.

    Retrieves the details of a specific post and renders them in the 'post_detail.html' template.

    Args:
    - request: HTTP request object.
    - slug: Unique identifier of the post.

    Returns:
    - Rendered response displaying details of the specified post.
    """
    post = get_object_or_404(Post, slug=slug)
    comments = PostComment.objects.filter(post=post).order_by('-id')
    form = CommentForm(request.POST or None)
    
    if post.subscription_required:
        user_subscription = UserSubscription.objects.filter(user=request.user).first()
        if not user_subscription or user_subscription.end_date < datetime.date.today():
            return redirect('subscription:subscriptions_list')
    
    if request.method == 'POST' and form.is_valid():
        text = form.cleaned_data['text']
        new_comment = PostComment(text=text, post=post, user=request.user)
        new_comment.save()
        messages.success(request, "Your comment has been added. Thank you")
        return HttpResponseRedirect(reverse('post-detail', kwargs={'slug': slug}))
    
    context = {'post': post, 'comments': comments, 'form': form}
    return render(request, 'core/post_detail.html', context)


@login_required
def post_create(request):
    """
    View for creating a new post.

    Allows authenticated users to create new posts.

    Args:
    - request: HTTP request object.

    Returns:
    - Redirects to the newly created post's detail page.
    """
    if request.user.userplan.plan.plan_type in ["Unlimited", "Standard"] or request.user.is_superuser:
        form = PostForm(request.POST or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return HttpResponseRedirect(reverse('post-detail', kwargs={'slug': post.slug}))
        
        context = {'form': form}
        return render(request, 'core/post_form.html', context)
    else:
        return HttpResponseRedirect(reverse('plan'))


@login_required
def post_update(request, slug):
    """
    View for updating an existing post.

    Allows authenticated users to update their own posts.

    Args:
    - request: HTTP request object.
    - slug: Unique identifier of the post to be updated.

    Returns:
    - Redirects to the updated post's detail page.
    """
    post = get_object_or_404(Post, slug=slug)
    if request.user != post.author:
        raise PermissionDenied
    
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('post-detail', kwargs={'slug': slug}))
    
    context = {'form': form}
    return render(request, 'core/post_form.html', context)


@login_required
def post_delete(request, slug):
    """
    View for deleting a post.

    Allows authenticated users to delete their own posts.

    Args:
    - request: HTTP request object.
    - slug: Unique identifier of the post to be deleted.

    Returns:
    - Redirects to the home page after deleting the post.
    """
    post = get_object_or_404(Post, slug=slug)
    if request.user != post.author:
        raise PermissionDenied
    
    post.delete()
    return HttpResponseRedirect('/')


def category(request, link):
    """
    View for displaying posts based on category.

    Retrieves posts based on the provided category and renders them in the 'projects.html' template.

    Args:
    - request: HTTP request object.
    - link: Category identifier.

    Returns:
    - Rendered response displaying posts of the specified category.
    """
    categories = {
        "graphics-design": "Graphics & Design",
        # ... (other category mappings)
    }
    try:
        posts = Post.objects.filter(category=categories.get(link))
        return render(request, 'core/projects.html', {'posts': posts})
    except KeyError:
        return redirect('home')


def search(request):
    """
    View for searching posts by title.

    Retrieves posts based on the provided title query and renders them in the 'post_search_results.html' template.

    Args:
    - request: HTTP request object.

    Returns:
    - Rendered response displaying search results.
    """
    query = request.GET.get('title')
    if query:
        posts = Post.objects.filter(title__icontains=query)
        context = {'posts': posts}
        return render(request, 'core/post_search_results.html', context)
    else:
        return redirect('home')


@login_required
def public_profile(request, username):
    """
    View for displaying the public profile of a user.

    Retrieves the public profile information and posts of the specified user and renders them in the 'public_profile.html' template.

    Args:
    - request: HTTP request object.
    - username: Username of the user whose profile is being viewed.

    Returns:
    - Rendered response displaying the public profile of the specified user.
    """
    obj = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author__username=obj).order_by('-date_posted')
    context = {'posts': posts, 'username': obj}
    return render(request, 'core/public_profile.html', context)


@login_required
def rate_post_view(request, slug, rating):
    """
    View for rating a post.

    Allows authenticated users to rate a post.

    Args:
    - request: HTTP request object.
    - slug: Unique identifier of the post to be rated.
    - rating: Rating value given by the user.

    Returns:
    - Redirects to the post's detail page after rating.
    """
    try:
        post = Post.objects.get(slug=slug)
        if post and not PostReview.objects.filter(user=request.user, post=post).exists():
            review = PostReview(post=post, user=request.user, rating=rating)
            review.save()
            post.last_rating = post.calc_rating
            post.save()
            messages.success(request, f'You rated a post: {post.title}')
        else:
            messages.warning(request, f'You already rated this post')
        return redirect('post-detail', slug=post.slug)
    except Post.DoesNotExist:
        raise Http404("Post is unavailable")


@login_required
def comment(request, slug):
    """
    View for commenting on a post.

    Allows authenticated users to comment on a post.

    Args:
    - request: HTTP request object.
    - slug: Unique identifier of the post to comment on.

    Returns:
    - Redirects to the post's detail page after commenting.
    """
    return redirect('post-detail', slug=slug)


def contact_create(request):
    """
    View for creating a contact message.

    Allows users to send contact messages.

    Args:
    - request: HTTP request object.

    Returns:
    - Redirects to the home page after sending the contact message.
    """
    form = ContactForm(request.POST or None)
    if form.is_valid():
        contact = form.save(commit=False)
        contact.author = request.user
        contact.save()
        return HttpResponseRedirect(reverse('home'))
    
    context = {'form': form}
    return render(request, 'core/contact_form.html', context)


def post_search_list(request):
    """
    View for searching posts.

    Retrieves posts based on the provided search query and renders them in the 'projects.html' template.

    Args:
    - request: HTTP request object.

    Returns:
    - Rendered response displaying search results.
    """
    result = Post.objects.order_by('-last_rating')
    query = request.GET.get('q')
    if query:
        query_list = query.split()
        result = result.filter(
            reduce(operator.and_,
                   (Q(title__icontains=q) for q in query_list)) |
            reduce(operator.and_,
                   (Q(overview__icontains=q) for q in query_list))
        )
    context = {'posts': result}
    return render(request, 'core/projects.html', context)
