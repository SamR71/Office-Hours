from django.db import models

# Create your models here.
class userSchedule(models.Model):
    user = models.TextField()
    courses = models.TextField