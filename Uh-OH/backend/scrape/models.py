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
	courseName = models.CharField(max_length=128)

	def __str__(self):
		return self.courseName

	def getSections():
		return self.CourseSection_set

class CourseSection(models.Model):
	"""
	CourseSection Class represents a single section of a Course
	by the Course, sectionID, and instructorName.
	"""
	class Meta:
		verbose_name = 'Course Section'
		verbose_name_plural = 'Course Sections'
        
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	sectionID = models.CharField(validators=[MinLengthValidator(2)], max_length = 2);
	instructorName = models.CharField(max_length=128)

	def __str__(self):
		return str(self.course) + " w/ Section: " + str(self.sectionID) + " + Instructor: " + str(self.instructorName)

