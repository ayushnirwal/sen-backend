from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Prof(models.Model):
    user_obj = models.ForeignKey(User, on_delete=models.CASCADE)
    courses = models.CharField(max_length=50)

class LecInstances(models.Model):
    date = models.DateTimeField( auto_now_add=True )
    course = models.CharField( max_length=50 )
    lec_hash = models.CharField( max_length=50 )

class AttendanceRecord(models.Model):
    date = models.DateTimeField( auto_now_add=True )
    studentID = models.CharField( max_length=50 )
    course = models.CharField( max_length=50 )
    lecID = models.CharField( max_length=50)

class ValidTokens(models.Model):
    token = models.CharField( max_length=50 )
    user_obj = models.ForeignKey(User, on_delete=models.CASCADE)

class Code(models.Model):
    code = models.CharField(max_length=50)
    course = models.CharField( max_length=50)

