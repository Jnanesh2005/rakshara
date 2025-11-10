from django.contrib import admin
from .models import User, School, StudentProfile, TeacherProfile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    pass

admin.site.register(School)
admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)
