from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, CandidateProfile, HirerProfile


class HirerRegistrationForm(UserCreationForm):
    company_name = forms.CharField(max_length=255)
    address = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'hirer'
        if commit:
            user.save()
            HirerProfile.objects.create(
                user=user,
                company_name=self.cleaned_data.get('company_name'),
                address=self.cleaned_data.get('address')
            )
        return user


class CandidateRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    location = forms.CharField(max_length=255)
    gender = forms.ChoiceField(choices=CandidateProfile.GENDER_CHOICES)
    resume = forms.CharField(widget=forms.Textarea, required=False)
    cv = forms.FileField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'candidate'
        if commit:
            user.save()
            CandidateProfile.objects.create(
                user=user,
                first_name=self.cleaned_data.get('first_name'),
                last_name=self.cleaned_data.get('last_name'),
                location=self.cleaned_data.get('location'),
                gender=self.cleaned_data.get('gender'),
                resume=self.cleaned_data.get('resume'),
                cv=self.cleaned_data.get('cv')
            )
        return user