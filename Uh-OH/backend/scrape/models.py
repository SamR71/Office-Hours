from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.
class Search(models.Model):
    searchValue = models.CharField(max_length=500)
    createTime = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Searches'

    def __str__(self):
        return self.searchValue

class Course(models.Model):
	"""Course Class represents a single course as its courseName."""
	#courseName = Listed Name of Course. 
	courseName = models.CharField(max_length=128)
	#courseValue = CRN Number.
	courseValue = models.CharField(validators=[MinLengthValidator(5)], max_length=5);
	#courseAbbrev = Abbreviation For Course Name.
	courseAbbrev = models.CharField(max_length=128)

	class Meta:
		verbose_name = 'Course'
		verbose_name_plural = 'Courses'

	def __str__(self):
		return self.courseName

class CourseSection(models.Model):
	"""
	CourseSection Class represents a single section of a Course
	by the Course, sectionID, and instructorName.
	"""
	class Meta:
		verbose_name = 'Course Section'
		verbose_name_plural = 'Course Sections'
        
	currentCourse = models.ForeignKey(Course, on_delete=models.CASCADE)
	sectionID = models.CharField(validators=[MinLengthValidator(2)], max_length = 2);

	def __str__(self):
		return str(self.currentCourse) + " + " + str(self.sectionID);

class CourseMeetingTime(models.Model):
	"""
	CourseMeetingTime Class represents a specific meeting time 
	of a CourseSection.
	"""
	class Meta:
		verbose_name = 'Course Meeting Time'
		verbose_name_plural = 'Course Meeting Times'
        
	meetSection = models.ForeignKey(CourseSection, on_delete=models.CASCADE)
	meetType = models.CharField(max_length=3)
	meetDates = models.CharField(max_length=7)
	meetStartTime = models.CharField(max_length=7)
	meetEndTime = models.CharField(max_length=7)
	meetInstructor = models.CharField(max_length=128, default = "")

	def __str__(self):
		return str(self.meetSection) + " + " + str(self.meetType) + " + " + str(self.meetInstructor);
