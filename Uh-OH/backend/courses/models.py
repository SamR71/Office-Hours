from django.db import models

# Create your models here.
class Course(models.Model):
	title = models.CharField(max_length=128)

	def __str__(self):
		return self.title

class CourseSection(models.Model):
	"""
	DAYS_OF_WEEK = (
        ('M', 'Monday'),
        ('T', 'Tuesday'),
        ('W', 'Wednesday'),
        ('R', 'Thursday'),
        ('F', 'Friday'),
    )
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
	section_id = models.IntegerField()
	instructor = models.CharField(max_length=128)

	def __str__(self):
		return self.course + self.section_id
