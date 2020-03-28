from django.db import models

# Create your models here.
class userScheduleItem(models.Model):
	"""
	CourseSection Class represents a single section of a Course
	by the Course, sectionID, and instructorName.
	"""
	class Meta:
		verbose_name = 'User Schedule Item'
		verbose_name_plural = 'User Schedule Items'
    
	#for whom is this an entry in their schedule
	username = models.CharField(max_length=50)
	
	
	#information about the given entry
	meetInstructor = models.CharField(max_length=50)
	meetStartTime = models.CharField(max_length=7)
	meetEndTime = models.CharField(max_length=7)
	meetLocation = models.CharField(max_length=23)
	meetDates = models.CharField(max_length=7)

	def __str__(self):
		return str(self.Instructor) + " + " + str(self.meetLocation) + " + " + str(self.meetDates) + " + " + str(self.meetStartTime) + " + " + str(self.meetEndTime)