from django.db import models

class ModelInfo(models.Model):
    name = models.CharField(max_length=100, default="Health AI Model")
    version = models.CharField(max_length=20, default="1.0")
    date_loaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} v{self.version}"
