from django.urls import path
from . import views

urlpatterns = [
    # 🏫 Teacher Dashboard (Main Page)
    path('', views.teacher_dashboard, name='teacher_dashboard'),

    # 👩‍🏫 View classroom details
    path('<int:pk>/', views.classroom_detail, name='classroom_detail'),

    # 🩺 Quick health check route
    path('<int:pk>/quick-check/', views.quick_checkup, name='quick_checkup'),

    # 📝 Join request approval/rejection
    path('approve/<int:pk>/', views.approve_request, name='approve_request'),
    path('reject/<int:pk>/', views.reject_request, name='reject_request'),
]
