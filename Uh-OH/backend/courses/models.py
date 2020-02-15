from django.db import models

# Create your models here.
class Course(models.Model):
	"""Course Class represents a single course as its title"""
	title = models.CharField(max_length=128)

	def __str__(self):
		return self.title

class CourseSection(models.Model):
	"""
	CourseSection Class represents a single section of a course
	by the course it's from, its title, its section id, and its instructor
	"""
	"""
		the following code will be used to handle holding days
		of the week when it becomes applicable
	DAYS_OF_WEEK = (
		('M', 'Monday'),
		('T', 'Tuesday'),
		('W', 'Wednesday'),
		('R', 'Thursday'),
		('F', 'Friday'),
	)
	"""
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	section_id = models.IntegerField()
	instructor = models.CharField(max_length=128)

	def __str__(self):
		return str(self.course) + " | section: " + str(self.section_id) + " | instructor: " + str(self.instructor)
