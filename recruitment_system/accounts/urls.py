from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/hirer/', views.register_hirer, name='register_hirer'),
    path('register/candidate/', views.register_candidate, name='register_candidate'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/hirer/', views.hirer_dashboard, name='hirer_dashboard'),
    path('dashboard/candidate/', views.candidate_dashboard, name='candidate_dashboard'),
    path('hirer_profile/', views.hirer_profile, name='hirer_profile'),
]