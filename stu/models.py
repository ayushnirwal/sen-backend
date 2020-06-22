from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Student(models.Model):
    user_obj = models.ForeignKey(User, on_delete=models.CASCADE)
    courses = models.CharField(max_length=50)