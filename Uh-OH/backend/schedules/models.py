from django.db import models

# Create your models here.
class userScheduleItem(models.Model):
	"""
	userScheduleItem Class represents a single schedule item for a user
	"""
	class Meta:
		verbose_name = 'User Schedule Item'
		verbose_name_plural = 'User Schedule Items'
    	
	#information about the given entry
	meetInstructor = models.CharField(max_length=50)
	meetStartTime = models.CharField(max_length=7)
	meetEndTime = models.CharField(max_length=7)
	meetLocation = models.CharField(max_length=23)
	meetDates = models.CharField(max_length=7)

	def __str__(self):
		return str(self.meetInstructor) + " + " + str(self.meetLocation) + " + " + str(self.meetDates) + " + " + str(self.meetStartTime) + " + " + str(self.meetEndTime)

class userSchedules(models.Model):
	"""
	userSchedules Class represents a database that associates usernames with schedules
	"""
	class Meta:
		verbose_name = 'User Schedule'
		verbose_name_plural = 'User Schedules'
    
	#for whom is this an entry in their schedule
	username = models.CharField(max_length=50)
	
	
	#concatenation of several different userScheduleItem strings
	schedule = models.CharField(max_length=200)

	def __str__(self):
		return str(self.schedule)