from operator import mod
from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    add_by = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    course_name = models.CharField(max_length=50)
    question_number = models.PositiveIntegerField()
    total_marks = models.PositiveIntegerField()
    invitedExamineEmail = models.TextField(blank=True)
    isViva = models.BooleanField(default=False, blank=True)
    def __str__(self):
        return self.course_name

class Question(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    marks=models.PositiveIntegerField()
    question=models.CharField(max_length=600)
    option1=models.CharField(max_length=200)
    option2=models.CharField(max_length=200)
    option3=models.CharField(max_length=200)
    option4=models.CharField(max_length=200)
    cat=(('Option1','Option1'),('Option2','Option2'),('Option3','Option3'),('Option4','Option4'))
    answer=models.CharField(max_length=200,choices=cat)


class Viva(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE,null=True,blank=True)
    marks=models.PositiveIntegerField(null=True,blank=True)
    question_link = models.TextField(null=True,blank=True)
    


class Result(models.Model):
    student = models.ForeignKey(User,on_delete=models.CASCADE)
    exam = models.ForeignKey(Course,on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()

    date = models.DateTimeField(auto_now=True)


class VivaResult(models.Model):
    student = models.ForeignKey(User,on_delete=models.CASCADE)
    exam = models.ForeignKey(Course,on_delete=models.CASCADE)
    marks = models.PositiveIntegerField(blank=True,null=True)
    date = models.DateTimeField(auto_now=True)
    answer_link = models.TextField(null=True,blank=True)

