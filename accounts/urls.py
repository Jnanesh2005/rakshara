from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # ✅ Home page route
    path('register/student/', views.student_register, name='student_register'),
    path('register/teacher/', views.teacher_register, name='teacher_register'),
    path('login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('verify-signup-otp/', views.verify_teacher_signup_otp, name='verify_teacher_signup_otp'),
    path('verify-login-otp/', views.verify_teacher_login_otp, name='verify_teacher_login_otp'),
    path('set-language/', views.set_language, name='set_language'),
    # New URLs for placeholder pages
    path('settings/', views.settings_page, name='settings'),
    path('help/', views.help_center_page, name='help_center'),
    path('faq/', views.faq_page, name='faq'),

]
