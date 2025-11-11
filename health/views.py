from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

from classroom.models import VirtualClassroom
from .models import VitalRecord
from accounts.models import StudentProfile, TeacherProfile
from ai_engine.utils import predict_health
from ai_engine.translate import get_translated_text
from accounts.models import StudentProfile, Notification, JoinRequest


# 🩺 ADD VITAL RECORD
@login_required
def add_vital_record(request, student_code=None):
    user = request.user
    if user.is_student:
        student_profile = user.student_profile
    else:
        if student_code:
            student_profile = get_object_or_404(StudentProfile, student_code=student_code)
        else:
            messages.error(request, "No student selected.")
            return redirect('teacher_dashboard')

    if request.method == 'POST':
        hr = int(request.POST.get('heart_rate'))
        spo2 = float(request.POST.get('spo2'))
        br = float(request.POST.get('breathing_rate'))
        temp = float(request.POST.get('temperature'))
        weight = request.POST.get('weight_kg') or student_profile.weight_kg
        height = request.POST.get('height_cm') or student_profile.height_cm

        score, label = predict_health(hr, spo2, br, temp, weight, height)

        VitalRecord.objects.create(
            student=student_profile,
            heart_rate=hr,
            spo2=spo2,
            breathing_rate=br,
            temperature_c=temp,
            weight_kg=weight,
            height_cm=height,
            prediction_score=score,
            prediction_label=label
        )

        # ✅ Return template with popup instead of redirect
        return render(request, 'health/add_vital.html', {
            'student': student_profile,
            'prediction_label': label,
            'prediction_score': score,
        })

    return render(request, 'health/add_vital.html', {'student': student_profile})

# 📊 STUDENT DASHBOARD
@login_required
def student_dashboard(request):
    """Displays student's health summary, charts, and recent records."""
    if not request.user.is_student:
        return redirect('teacher_dashboard')

    profile = request.user.student_profile

    # ✅ Query ordered vitals properly
    vitals_qs = profile.vitals.all().order_by('-recorded_at')
    latest_vital = vitals_qs.first()  # Safe latest record
    vitals = list(vitals_qs[:30])     # Recent 30 records

    # Prepare data for chart (reverse for chronological order)
    labels = [v.recorded_at.strftime("%d %b %H:%M") for v in reversed(vitals)]
    hr_data = [v.heart_rate for v in reversed(vitals)]
    spo2_data = [v.spo2 for v in reversed(vitals)]
    temp_data = [v.temperature_c for v in reversed(vitals)]

    return render(request, 'health/student_dashboard.html', {
        'profile': profile,
        'vitals': vitals,
        'latest_vital': latest_vital,
        'labels': labels,
        'hr_data': hr_data,
        'spo2_data': spo2_data,
        'temp_data': temp_data
    })


# 🧑‍🏫 TEACHER DASHBOARD
@login_required
def teacher_dashboard(request):
    """Display teacher dashboard with classes, notifications, and pending join requests."""
    teacher = request.user
    school = getattr(teacher, 'school', None)

    # ✅ Restrict to teachers only
    if not getattr(teacher, "is_teacher", False):
        messages.error(request, "Access denied: only teachers can access this page.")
        return redirect('student_dashboard')

    # ✅ Notifications
    notifications = Notification.objects.filter(teacher=teacher).order_by('-created_at')
    unread_count = notifications.filter(is_read=False).count()
    Notification.objects.filter(teacher=teacher, is_read=False).update(is_read=True)

    # ✅ Virtual classes
    classes = VirtualClassroom.objects.filter(teacher=teacher)

    # ✅ Pending join requests (students waiting for approval)
    pending_requests = JoinRequest.objects.filter(
        teacher=teacher, approved=False
    ).select_related('student__user')

    # ✅ Handle new class creation
    if request.method == 'POST':
        class_name = request.POST.get('class_name')
        section = request.POST.get('section')

        if not school:
            messages.error(request, 'You are not assigned to any school.')
            return redirect('teacher_dashboard')

        if VirtualClassroom.objects.filter(school=school, class_name=class_name, section=section).exists():
            messages.warning(request, f"⚠️ Class {class_name}-{section} already exists.")
        else:
            vc = VirtualClassroom.objects.create(
                school=school,
                teacher=teacher,
                class_name=class_name,
                section=section
            )
            messages.success(request, f"🏫 Class {vc.class_name}-{vc.section} created successfully!")

        return redirect('teacher_dashboard')

    # ✅ Add student counts
    for c in classes:
        c.student_count = c.students.count()

    return render(
        request,
        'health/teacher_dashboard.html',
        {
            'classes': classes,
            'notifications': notifications,
            'unread_count': unread_count,
            'pending_requests': pending_requests,
        }
    )
