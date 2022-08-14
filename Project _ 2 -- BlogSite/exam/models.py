from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image


# Create your models here.
class Exams(models.Model):
	title = models.CharField(max_length=200)
	full_marks = models.IntegerField()
	content = models.TextField()
	date = models.DateTimeField(default=timezone.now)
	time = models.IntegerField()
	evaluator = models.ForeignKey(User,on_delete=models.CASCADE)
	examine = models.ManyToManyField(User)


	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('blogPosts:postDetail', kwargs = {'pk':self.pk})