# health/urls.py
from django.urls import path
from . import views

app_name = 'health' # <-- Add this line

urlpatterns = [
    path('add/', views.add_vital_record, name='add_vital'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('add/<str:student_code>/', views.add_vital_record, name='add_vital_for_student'),
]