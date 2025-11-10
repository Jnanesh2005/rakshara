from django.db import models
from accounts.models import School, StudentProfile, User
from django.utils import timezone

class VirtualClassroom(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='virtual_classes')
    class_name = models.CharField(max_length=50)
    section = models.CharField(max_length=10)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='classes_teaching')
    students = models.ManyToManyField(StudentProfile, blank=True, related_name='virtual_classes')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('school', 'class_name', 'section')

    def __str__(self):
        return f"{self.school.name} - {self.class_name}{self.section}"
