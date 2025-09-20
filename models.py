from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = (('Teacher', 'Teacher'), ('Student', 'Student'))
    role = models.CharField(choices=ROLE_CHOICES, max_length=10)

    

class Test(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    is_public = models.BooleanField(default=True)
    code = models.CharField(max_length=10, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=1,blank=True, null=True)

class StudentAnswer(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, default=1)  

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    submitted_answer = models.CharField(max_length=1)


