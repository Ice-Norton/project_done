from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.job_list, name='job_list'),
    path('create/', views.create_job, name='create_job'),
    path('update/<int:job_id>/', views.update_job, name='update_job'),
    path('delete/<int:job_id>/', views.delete_job, name='delete_job'),
    path('my-jobs/', views.hirer_jobs, name='hirer_jobs'),
    path('apply/<int:job_id>/', views.apply_for_job, name='apply_for_job'),
    path('applications/', views.candidate_applications, name='candidate_applications'),
    path('jobs/', views.job_applications, name='job_applications'),
    path('application/<int:application_id>/<str:status>/', views.update_application_status, name='update_application_status'),
]