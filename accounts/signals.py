from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StudentProfile, User ,TeacherProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    This is the ONLY signal we need.
    It creates a new profile when a new user is created.
    """
    if created:
        if instance.is_student:
            StudentProfile.objects.create(user=instance)
        elif instance.is_teacher:
            TeacherProfile.objects.create(user=instance)
@receiver(post_save, sender=User)
def create_teacher_profile(sender, instance, created, **kwargs):
    if created and instance.is_teacher:
        from .models import TeacherProfile
        TeacherProfile.objects.create(user=instance)
