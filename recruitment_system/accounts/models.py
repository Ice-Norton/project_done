from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.urls import reverse


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('hirer', 'Hirer'),
        ('candidate', 'Candidate'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    email = models.EmailField(unique=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class HirerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='hirer_profile')
    company_name = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return f"{self.company_name}"

    def get_absolute_url(self):
        return reverse('job_applications', kwargs={'job_id': self.id})


class CandidateProfile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='candidate_profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    resume = models.TextField(default=False)
    cv =models.FileField(upload_to="resume/", default=False)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"