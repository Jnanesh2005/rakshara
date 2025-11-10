from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StudentProfile, User


@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    if created and instance.is_student:
        StudentProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def create_teacher_profile(sender, instance, created, **kwargs):
    if created and instance.is_teacher:
        from .models import TeacherProfile
        TeacherProfile.objects.create(user=instance)
