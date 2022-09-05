
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser, User
from courses.models import Course

# Create your models here.


"""
class User(AbstractUser):
	
	bio = models.CharField(max_length = 2000)
	profile = models.ImageField()
	dob = models.DateField()
	full_name = models.CharField(max_length = 500)
	linkedIn = models.URLField(max_length = 500, null = True, blank = True)



"""


class CourseStatus(models.Model):

	CHOICES = [('Favourite', 'Favourite'), ('Doing', 'Doing'), ('Done', 'Done'), ('Bought', 'Bought')]

	user = models.ForeignKey(User, on_delete = models.CASCADE)
	course = models.ForeignKey(Course, on_delete = models.CASCADE)
	status = models.CharField(max_length = 25)

	def __str__(self):
		return f"{self.user}'s status for {self.course.name} is {self.status}"
