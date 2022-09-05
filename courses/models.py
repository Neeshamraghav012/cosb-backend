from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from taggit.managers import TaggableManager

class Course(models.Model):

	CHOICES = (

		('Videos', 'Videos'),
		('Textual', 'Textual'),
		('Hybrid', 'Hybrid'),
	)

	name = models.CharField(max_length = 1000)
	author = models.CharField(max_length = 1000)
	tags = TaggableManager(related_name="course_tags")
	enrolls = models.CharField(max_length = 25)
	description = models.TextField()
	image_mobile = models.URLField(max_length = 500, null = True, blank = True)
	image = models.URLField(max_length = 500, null = True, blank = True)
	link = models.URLField(max_length = 2000)
	overall_rating = models.FloatField(default = 0)
	total_ratings = models.IntegerField(default = 0)
	price = models.IntegerField(default = 0)
	catagory = models.CharField(max_length = 250, default="Computer Science")
	platform = models.CharField(max_length = 1000, default="YouTube")
	university = models.CharField(max_length = 1000, blank = True)
	released_date = models.DateField(auto_now_add = True)
	country = models.CharField(max_length = 1000, default="India")
	language = models.CharField(max_length = 250, default="English")
	duration = models.IntegerField(default=4)
	certificate = models.BooleanField(default = False)
	material_type = models.CharField(max_length = 25, choices = CHOICES, default="Videos")
	added_by = models.CharField(max_length = 1000, default="Neesham")
	num_of_reviews = models.IntegerField(default = 0)
	num_of_ratings = models.IntegerField(default = 0)
	# views = models.IntegerField(default = 0)


	def __str__(self):
		return f"{self.name}"

	class  Meta:

		verbose_name_plural = "Courses"
		ordering = ["-overall_rating"]


class Ratings(models.Model):

	user = models.ForeignKey(User, on_delete = models.CASCADE)
	course = models.ForeignKey(Course, on_delete = models.CASCADE)
	review = models.TextField()
	rating = models.FloatField(default = 0)


	def __str__(self):
		return f"{self.user.username} rated Course {self.course.name}"


	# make a function to add this user rating to the course
	def update_rating(self):
		course = Course.objects.get(id = self.course.id)
		ratings = Ratings.objects.filter(course = course)

		course.total_ratings += self.rating
		course.overall_rating = (course.total_ratings / len(ratings))
		course.save()
