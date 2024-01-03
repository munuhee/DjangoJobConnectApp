"""
Views for managing jobs and bids within the application.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Job, Bid
from .forms import JobForm, BidForm

def job_list(request):
    """
    View function to display a list of jobs.
    """
    jobs = Job.objects.all()
    return render(request, 'jobs/job_list.html', {'jobs': jobs})

def job_detail(request, job_id):
    """
    View function to display details of a specific job and handle bids.
    """
    job = get_object_or_404(Job, pk=job_id)
    bid_form = BidForm(request.POST or None)
    bids = Bid.objects.filter(job=job)
    
    # Get the count of bids for the job
    bids_count = bids.count()

    if request.method == 'POST':
        if bid_form.is_valid():
            bid_instance = bid_form.save(commit=False)
            bid_instance.job = job
            bid_instance.bidder = request.user
            bid_instance.save()
            messages.success(request, 'Your bid has been submitted successfully!')
            return redirect('job_detail', job_id=job_id)
        else:
            for field, errors in bid_form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")

    return render(
        request,
        'jobs/job_detail.html',
        {
            'job': job,
            'bid_form': bid_form,
            'bids': bids,
            'bids_count': bids_count
        }
    )

def submit_bid(request, job_id):
    """
    View function to handle bid submission.
    """
    job = get_object_or_404(Job, pk=job_id)
    if request.method == 'POST':
        bid_form = BidForm(request.POST)
        if bid_form.is_valid():
            bid_instance = bid_form.save(commit=False)
            bid_instance.job = job
            bid_instance.bidder = request.user
            bid_instance.save()
            messages.success(request, 'Your bid has been submitted successfully!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            for field, errors in bid_form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def job_create(request):
    """
    View function to create a new job.
    """
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.author = request.user
            job.save()
            messages.success(request, 'Job created successfully!')
            return redirect('job_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    else:
        form = JobForm()
    return render(request, 'jobs/job_create.html', {'form': form})

def job_update(request, job_id):
    """
    View function to update an existing job.
    """
    job = get_object_or_404(Job, pk=job_id)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully!')
            return redirect('job_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    else:
        form = JobForm(instance=job)
    return render(request, 'jobs/job_update.html', {'form': form, 'job': job})

def job_delete(request, job_id):
    """
    View function to delete a job.
    """
    job = get_object_or_404(Job, pk=job_id)
    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job deleted successfully!')
        return redirect('job_list')
    return render(request, 'jobs/job_delete.html', {'job': job})
