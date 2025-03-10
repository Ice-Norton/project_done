from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Job, Application
from .forms import JobForm
from django.contrib import messages


@login_required
def job_list(request):
    search_query = request.GET.get('q', '')
    location_filter = request.GET.get('location', '')
    sort_by = request.GET.get('sort', 'newest')
    jobs = Job.objects.all()
    if search_query:
        jobs = jobs.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(requirements__icontains=search_query)
        )

    if location_filter:
        jobs = jobs.filter(location__icontains=location_filter)

    if sort_by == 'newest':
        jobs = jobs.order_by('-created_at')
    elif sort_by == 'oldest':
        jobs = jobs.order_by('created_at')
    elif sort_by == 'salary_high':
        jobs = jobs.order_by('-salary_max', '-salary_min')
    elif sort_by == 'salary_low':
        jobs = jobs.order_by('salary_min', 'salary_max')
    return render(request, 'job_list.html', {'jobs': jobs})


@login_required
def create_job(request):
    if request.user.user_type != 'hirer':
        return redirect('home')

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.hirer = request.user
            job.save()
            return redirect('hirer_jobs')
    else:
        form = JobForm()
    return render(request, 'job_form.html', {'form': form})


@login_required
def update_job(request, job_id):
    if request.user.user_type != 'hirer':
        return redirect('home')

    job = get_object_or_404(Job, id=job_id, hirer=request.user)

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('hirer_jobs')
    else:
        form = JobForm(instance=job)
    return render(request, 'job_form.html', {'form': form})


@login_required
def delete_job(request, job_id):
    if request.user.user_type != 'hirer':
        return redirect('home')

    job = get_object_or_404(Job, id=job_id, hirer=request.user)

    if request.method == 'POST':
        job.delete()
        return redirect('hirer_jobs')

    return render(request, 'job_confirm_delete.html', {'job': job})


@login_required
def hirer_jobs(request):

    # Get filter parameters
    status_filter = request.GET.get('status', 'all')
    search_query = request.GET.get('q', '')

    # Get user's jobs
    jobs = Job.objects.filter(hirer=request.user)

    # Apply filters
    if status_filter and status_filter != 'all':
        jobs = jobs.filter(status=status_filter)

    if search_query:
        jobs = jobs.filter(title__icontains=search_query)

    # Get job statistics
    total_jobs = Job.objects.filter(hirer=request.user).count()
    active_jobs = Job.objects.filter(hirer=request.user, status='open').count()
    draft_jobs = Job.objects.filter(hirer=request.user, status='draft').count()
    total_applications = Application.objects.filter(job__hirer=request.user).count()

    context = {
        'jobs': jobs,
        'total_jobs': total_jobs,
        'active_jobs': active_jobs,
        'draft_jobs': draft_jobs,
        'total_applications': total_applications,
        'status_filter': status_filter,
        'search_query': search_query,

    }

    return render(request, 'hirer_jobs.html', context)



@login_required
def apply_for_job(request, job_id):
    if request.user.user_type != 'candidate':
        return redirect('home')

    job = get_object_or_404(Job, id=job_id)

    # Check if already applied
    existing_application = Application.objects.filter(job=job, candidate=request.user).first()
    if existing_application:
        messages.warning(request, 'You have already applied for this job.')
        return redirect('job_list')

    Application.objects.create(job=job, candidate=request.user)
    messages.success(request, 'Your application has been submitted.')
    return redirect('candidate_applications')


@login_required
def candidate_applications(request):
    status_filter = request.GET.get('status', '')
    search_query = request.GET.get('q', '')

    if request.user.user_type != 'candidate':
        return redirect('home')

    applications = Application.objects.filter(candidate=request.user)
    if status_filter:
        applications = applications.filter(status=status_filter)

    if search_query:
        applications = applications.filter(
            Q(job__title__icontains=search_query) |
            Q(job__hirer__hirer_profile__company_name__icontains=search_query) |
            Q(job__location__icontains=search_query)
        )
    total_applications = Application.objects.filter(candidate=request.user).count()
    pending_applications = Application.objects.filter(candidate=request.user, status='pending').count()
    accepted_applications = Application.objects.filter(candidate=request.user, status='accepted').count()
    rejected_applications = Application.objects.filter(candidate=request.user, status='rejected').count()
    context = {
        'applications': applications,
        'status_filter': status_filter,
        'search_query': search_query,
        'total_applications': total_applications,
        'pending_applications': pending_applications,
        'accepted_applications': accepted_applications,
        'rejected_applications': rejected_applications,

    }
    return render(request, 'candidate_applications.html', context)

@login_required
def job_applications(request):
    if request.user.user_type != 'hirer':
        return redirect('home')

    status_filter = request.GET.get('status', 'all')
    job_filter = request.GET.get('job', '')
    search_query = request.GET.get('q', '')

    # Get applications for this hirer's jobs
    applications = Application.objects.filter(job__hirer=request.user)

    if status_filter and status_filter != 'all':
        applications = applications.filter(status=status_filter)

    if job_filter:
        applications = applications.filter(job_id=job_filter)

    if search_query:
        applications = applications.filter(
            Q(candidate__username__icontains=search_query) |
            Q(candidate__candidate_profile__first_name__icontains=search_query) |
            Q(candidate__candidate_profile__last_name__icontains=search_query)
        )

    user_jobs = Job.objects.filter(hirer=request.user)

    total_applications = applications.count()
    pending_applications = applications.filter(status='pending').count()
    accepted_applications = applications.filter(status='accepted').count()
    rejected_applications = applications.filter(status='rejected').count()

    context = {
        'applications': applications,
        'user_jobs': user_jobs,
        'total_applications': total_applications,
        'pending_applications': pending_applications,
        'accepted_applications': accepted_applications,
        'rejected_applications': rejected_applications,
        'status_filter': status_filter,
        'job_filter': job_filter,
        'search_query': search_query,
    }

    return render(request, 'job_applications.html', context)


@login_required
def update_application_status(request, application_id, status):
    if request.user.user_type != 'hirer':
        return redirect('home')

    application = get_object_or_404(Application, id=application_id, job__hirer=request.user)

    if status in ['accepted', 'rejected', 'pending']:
        application.status = status
        application.save()
        
    return redirect('job_applications')