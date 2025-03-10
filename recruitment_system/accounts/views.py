from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import HirerRegistrationForm, CandidateRegistrationForm
from jobs.models import Application, Job


def home(request):
    return render(request=request, template_name='home.html')

def hirer_profile(request):
    return render(request, template_name="hirer_profile.html", context={})


def register_hirer(request):
    if request.method == 'POST':
        form = HirerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('hirer_dashboard')
    else:
        form = HirerRegistrationForm()
    return render(request, template_name='hregister.html', context={'form': form, 'user_type': 'hirer'})


def register_candidate(request):
    if request.method == 'POST':
        form = CandidateRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('candidate_dashboard')
    else:
        form = CandidateRegistrationForm()
    return render(request, template_name='cregister.html', context={'form': form, 'user_type': 'candidate'})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.user_type == 'hirer':
                    return redirect('hirer_dashboard')
                else:
                    return redirect('candidate_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, template_name='user_login.html', context={'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def hirer_dashboard(request):
    if request.user.user_type != 'hirer':
        return redirect('home')
    active_jobs = Job.objects.filter(hirer=request.user, status='draft')
    active_jobs_count = active_jobs.count()
    total_applications = Application.objects.filter(job__hirer=request.user)
    total_applications_count = total_applications.count()
    pending_applications = total_applications.filter(status='pending')
    pending_applications_count = pending_applications.count()
    accepted_applications = total_applications.filter(status='accepted')
    accepted_applications_count = accepted_applications.count()
    recent_jobs = Job.objects.filter(hirer=request.user).order_by('-created_at')[:5]
    recent_applications = Application.objects.filter(job__hirer=request.user).order_by('-applied_at')[:5]
    return render(request, template_name='hirer_dashboard.html', context={'total_applications_count': total_applications_count, 'pending_applications_count': pending_applications_count, 'accepted_applications_count': accepted_applications_count, 'recent_jobs': recent_jobs, 'recent_applications': recent_applications, 'active_jobs_count': active_jobs_count})


@login_required
def candidate_dashboard(request):
    if request.user.user_type != 'candidate':
        return redirect('home')
    applications = Application.objects.filter(candidate=request.user)
    total_applications_count = applications.count()
    pending_applications = applications.filter(status='pending')
    pending_applications_count = pending_applications.count()
    accepted_applications = applications.filter(status='accepted')
    accepted_applications_count = accepted_applications.count()
    rejected_applications = applications.filter(status='rejected')
    rejected_applications_count = rejected_applications.count()
    return render(request, template_name='candidate_dashboard.html', context={'total_applications_count': total_applications_count, 'pending_applications_count': pending_applications_count, 'accepted_applications_count': accepted_applications_count, 'rejected_applications_count': rejected_applications_count})