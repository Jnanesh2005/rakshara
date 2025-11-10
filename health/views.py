from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import VitalRecord
from accounts.models import StudentProfile, TeacherProfile
from .utils import predict_health
from django.contrib import messages
from django.http import JsonResponse

@login_required
def add_vital_record(request, student_code=None):
    # Students add to themselves; teachers can pass student_code to add for that student
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
        weight = request.POST.get('weight_kg') or None
        height = request.POST.get('height_cm') or None
        weight = float(weight) if weight else student_profile.weight_kg
        height = float(height) if height else student_profile.height_cm

        score, label = predict_health(hr, spo2, br, temp, weight, height)
        rec = VitalRecord.objects.create(
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
        messages.success(request, f"Vitals saved. Prediction: {score} ({label})")
        # redirect to student view or to quick-check next student
        next_url = request.POST.get('next') or 'student_dashboard'
        return redirect(next_url)

    # GET => show form
    return render(request, 'health/add_vital.html', {'student': student_profile})

@login_required
def student_dashboard(request):
    if not request.user.is_student:
        return redirect('teacher_dashboard')
    profile = request.user.student_profile
    vitals = profile.vitals.all()[:30]
    # prepare data for chart
    labels = [v.recorded_at.strftime("%d %b %H:%M") for v in reversed(vitals)]
    hr_data = [v.heart_rate for v in reversed(vitals)]
    spo2_data = [v.spo2 for v in reversed(vitals)]
    temp_data = [v.temperature_c for v in reversed(vitals)]
    return render(request, 'health/student_dashboard.html', {
        'profile': profile,
        'vitals': vitals,
        'labels': labels,
        'hr_data': hr_data,
        'spo2_data': spo2_data,
        'temp_data': temp_data
    })


@login_required
def teacher_dashboard(request):
    # Get the teacher profile of the logged-in user
    teacher = get_object_or_404(TeacherProfile, user=request.user)
    school = teacher.user.school

    # Get all students belonging to the same school
    students = StudentProfile.objects.filter(user__school=school).order_by('class_name', 'section', 'roll_no')

    if request.method == 'POST':
        # Quick checkup form submission
        student_id = request.POST.get('student_id')
        heart_rate = request.POST.get('heart_rate')
        spo2 = request.POST.get('spo2')
        breathing_rate = request.POST.get('breathing_rate')
        temperature = request.POST.get('temperature')

        try:
            student = StudentProfile.objects.get(id=student_id)
            VitalRecord.objects.create(
                student=student,
                heart_rate=heart_rate,
                spo2=spo2,
                breathing_rate=breathing_rate,
                temperature=temperature,
            )
            messages.success(request, f"✅ Vitals added for {student.user.username}")
        except StudentProfile.DoesNotExist:
            messages.error(request, "❌ Student not found.")

        return redirect('teacher_dashboard')  # refresh the dashboard after POST

    context = {
        'teacher': teacher,
        'students': students,
    }
    return render(request, 'health/teacher_dashboard.html', context)