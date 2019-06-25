from django.db import models
from django.utils import timezone


class Recognition(models.Model):
    recognition_text = models.CharField(max_length=200)
    recognition_date = models.DateTimeField(default=timezone.now)
    pub_date = models.DateTimeField(default=timezone.now)
