from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import StudentSignUpForm, TeacherSignUpForm
from .models import School, StudentProfile, User, TeacherProfile, Notification, JoinRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout


# 🧩 STUDENT REGISTRATION
def student_register(request):
    if request.method == "POST":
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_student = True
            user.school = form.cleaned_data['school']
            user.save()

            # Update student profile
            profile = user.student_profile
            profile.roll_no = form.cleaned_data.get('roll_no')
            profile.dob = form.cleaned_data.get('dob')
            profile.height_cm = form.cleaned_data.get('height_cm')
            profile.weight_kg = form.cleaned_data.get('weight_kg')
            profile.personal_contact = form.cleaned_data.get('personal_contact')
            profile.parent_contact = form.cleaned_data.get('parent_contact')
            profile.address = form.cleaned_data.get('address')
            profile.class_name = form.cleaned_data.get('class_name')
            profile.section = form.cleaned_data.get('section')
            profile.save()

            # ✅ Notify teachers (create join request)
            teachers = TeacherProfile.objects.filter(user__school=user.school)
            found = False
            for teacher in teachers:
                if teacher.user.classes_teaching.filter(class_name=profile.class_name, section=profile.section).exists():
                    Notification.objects.create(
                        teacher=teacher.user,
                        message=f"🆕 New student {user.get_full_name() or user.username} requested to join class {profile.class_name}-{profile.section}."
                    )
                    JoinRequest.objects.create(
                        student=profile,
                        teacher=teacher.user,
                        class_name=profile.class_name,
                        section=profile.section
                    )
                    found = True
            if not found:
                Notification.objects.create(
                    message=f"🆕 New student {user.get_full_name() or user.username} registered (no assigned teacher yet)."
                )

            login(request, user)
            messages.success(request, f"✅ Account created successfully! Your Student ID: {profile.student_code}")
            return redirect('student_dashboard')
        messages.error(request, "Please correct the errors below.")
    else:
        form = StudentSignUpForm()
    return render(request, 'accounts/student_register.html', {'form': form})


# 🧩 TEACHER REGISTRATION
def teacher_register(request):
    if request.method == "POST":
        form = TeacherSignUpForm(request.POST)
        if form.is_valid():
            verification_id = form.cleaned_data['verification_id']
            school = form.cleaned_data['school']

            if school.school_code != verification_id:
                form.add_error('verification_id', '❌ Verification ID does not match school records')
            else:
                user = form.save(commit=False)
                user.is_teacher = True
                user.school = school
                user.save()

                profile = user.teacher_profile
                profile.contact = form.cleaned_data.get('contact')
                profile.address = form.cleaned_data.get('address')
                profile.verification_id = verification_id
                profile.save()

                login(request, user)
                messages.success(request, f"✅ Welcome, {user.username}! You’ve been registered as a teacher.")
                return redirect('teacher_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = TeacherSignUpForm()
    return render(request, 'accounts/teacher_register.html', {'form': form})


# 🏠 HOME
def home(request):
    user = request.user
    if user.is_authenticated:
        if getattr(user, "is_teacher", False):
            return redirect('teacher_dashboard')
        elif getattr(user, "is_student", False):
            return redirect('student_dashboard')
    return render(request, 'home.html')


# 🔐 LOGIN
def login_view(request):
    if request.method == "POST":
        username_or_id = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username_or_id, password=password)

        if user is None:
            try:
                student = StudentProfile.objects.get(student_code=username_or_id)
                user = authenticate(request, username=student.user.username, password=password)
            except StudentProfile.DoesNotExist:
                pass

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            if getattr(user, "is_student", False):
                return redirect('student_dashboard')
            elif getattr(user, "is_teacher", False):
                return redirect('teacher_dashboard')
            return redirect('home')

        messages.error(request, "❌ Invalid username, student ID, or password.")
    return render(request, "accounts/login.html")


# 🚪 LOGOUT
def logout_view(request):
    django_logout(request)
    messages.info(request, "👋 You have been logged out successfully.")
    return redirect('home')
