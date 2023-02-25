from django.shortcuts import render, reverse, get_object_or_404
from django.views.generic.base import View
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.list import ListView
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.core import serializers
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Job, Application
import operator
from django.core import serializers
from functools import reduce
from django.db.models import Q

class PageContextMixin(object):
    page_title = None
    def get_context_data(self, **kwargs):
        context = super(PageContextMixin, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context

class Home(PageContextMixin, ListView):
    model = Job
    template_name = 'jobs/home.html'
    context_object_name = 'jobs'
    ordering = '-pub_date'
    paginate_by = 6



def jobscategory(request, link):
    jobscategories = {
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
        jobs = Job.objects.filter(jobscategory=jobscategories[link])
        return render(request, 'jobs/home.html', {"jobs": jobs})
    except KeyError:
        return redirect('jobs')


class JobDisplay(PageContextMixin, SingleObjectMixin, View):
    model = Job
    context_object_name = 'j'
    page_title = 'Detail'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.save()
        job = self.get_context_data(object=self.object)
        return render(request, 'jobs/job_detail.html', job)

    def get_context_data(self, **kwargs):
        context = super(JobDisplay, self).get_context_data(**kwargs)
        return context

class JobDetail(DetailView):
    model = Job
    context_object_name = 'applications'

    def get(self, request, *args, **kwargs):
        view = JobDisplay.as_view()
        return view(request, *args, **kwargs)

    def job(self, request, *args, **kwargs):
        view = Application.as_view()
        return view(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class JobCreate(CreateView):
    model = Job
    fields = ('title', 'jobscategory','description', 'budget', 'status')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super(JobCreate, self).form_valid(form)



@method_decorator(login_required, name='dispatch')
class JobUpdate(UpdateView):
    model = Job
    fields = ('title', 'jobscategory','description', 'budget', 'status')


@method_decorator(login_required, name='dispatch')
class JobDelete(DeleteView):
    model = Job
    success_url = reverse_lazy('home')


class ApplicationCreateView(LoginRequiredMixin, CreateView):
    model = Application
    fields = ('content', 'budget')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.job = Job.objects.get(pk=self.kwargs['pk'])  # ['pk'] is the pk assigned by to the comment button in the home.html. we are making the instance of the form assign the post field of the comment model to the Post object whos pk=self.kwargs['pk'] which is the storage location of url parameters
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        if request.user.userplan.plan.plan_type == "Unlimited" or request.user.userplan.plan.plan_type == "Standard":
            if not request.user.is_authenticated:
                return HttpResponseForbidden()
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        else:
            return HttpResponseRedirect(reverse('plan'))


class ApplicationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Application
    fields = ('content', 'budget')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        application = self.get_object()
        if self.request.user == application.author:
            return True
        return False


class ApplicationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Application
    success_url = '/'

    def test_func(self):
        application = self.get_object()
        if self.request.user == application.author:
            return True
        return False



class JobSearchListView(Home):
    """
    Display a Blog List page filtered by the search query.
    """
    paginate_by = 6

    def get_queryset(self):
        result = super(JobSearchListView, self).get_queryset()

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