from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from taggit.managers import TaggableManager


# Create your models here.

class RoadMap(models.Model):

	user = models.ForeignKey(User, on_delete = models.CASCADE)
	image = models.URLField(max_length = 500, null = True, blank = True)
	reading_time = models.IntegerField(default = 0)
	title = models.CharField(max_length = 1000)
	desc = models.TextField()
	tags = TaggableManager(related_name="roadmap_tags")
	upvotes = models.IntegerField(default = 0)
	downvotes = models.IntegerField(default = 0)
	views = models.IntegerField(default = 0)
	timestamp = models.DateTimeField(auto_now_add = True, null = True)


	def __str__(self):
		return f"{self.title}"


	class  Meta:
		ordering = ["-upvotes"]
