from django import forms
from .models import Job, Application

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'location', 'salary_min', 'salary_max', 'requirements']

class ApplicationUpdateForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status']