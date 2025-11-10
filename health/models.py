from django.db import models
from accounts.models import StudentProfile
from django.utils import timezone

class VitalRecord(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='vitals')
    recorded_at = models.DateTimeField(default=timezone.now)
    heart_rate = models.IntegerField()  # bpm
    spo2 = models.FloatField()          # %
    breathing_rate = models.FloatField() # breaths per min
    temperature_c = models.FloatField()  # celsius
    weight_kg = models.FloatField(null=True, blank=True)
    height_cm = models.FloatField(null=True, blank=True)
    # computed prediction score and label
    prediction_score = models.FloatField(null=True, blank=True)  # 0-100
    prediction_label = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['-recorded_at']

    def __str__(self):
        return f"{self.student} @ {self.recorded_at.strftime('%Y-%m-%d %H:%M')}"
