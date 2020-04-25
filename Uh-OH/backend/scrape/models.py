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
	courseValue = models.CharField(validators=[MinLengthValidator(5)], max_length=5)
	#courseAbbrev = Abbreviation For Course Name.
	courseAbbrev = models.CharField(max_length=128)

	class Meta:
		verbose_name = 'Course'
		verbose_name_plural = 'Courses'

	def __str__(self):
		return self.courseName

class CourseSection(models.Model):
	"""
	CourseSection Class represents a 
	Single Section of a Course, specified by 
	the Course, sectionID, and instructorName.
	"""
	class Meta:
		verbose_name = 'Course Section'
		verbose_name_plural = 'Course Sections'
		
	currentCourse = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')
	sectionID = models.CharField(validators=[MinLengthValidator(2)], max_length = 2)

	def __str__(self):
		return str(self.currentCourse) + " + " + str(self.sectionID)

class CourseMeetingTime(models.Model):
	"""
	CourseMeetingTime Class represents a 
	specific Meeting Time of a CourseSection.
	"""
	class Meta:
		verbose_name = 'Course Meeting Time'
		verbose_name_plural = 'Course Meeting Times'
		
	meetSection = models.ForeignKey(CourseSection, on_delete=models.CASCADE, related_name='courseMeetingTimes')
	meetType = models.CharField(max_length=3)
	meetDates = models.CharField(max_length=7)
	meetStartTime = models.CharField(max_length=7)
	meetEndTime = models.CharField(max_length=7)
	meetInstructor = models.CharField(max_length=128, default = "")

	def __str__(self):
		return str(self.meetSection) + " + " + str(self.meetType) + " + " + str(self.meetInstructor)


class Instructor(models.Model):
	"""
	Instructor Class represents a 
	specific Instructor linked to a specific
	Course Object, specified by:
	Course, Name, Email.
	"""
	class Meta:
		verbose_name = 'Instructor'
		verbose_name_plural = 'Instructor'

	iType = models.CharField(max_length=1)
	iName = models.CharField(max_length=128)
	iEmail = models.CharField(max_length=128)
	currentCourse = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='instructors')

	def __str__(self):
		fullInstructorType = "Professor"
		if(self.iType == "T"):
			fullInstructorType = "Teaching Assistant"
		return str(self.currentCourse) + " + " + fullInstructorType + " + " + str(self.iName) + " + " + str(self.iEmail)

class InstructorOfficeHours(models.Model):
	"""
	InstructorOfficeHours Class represents a 
	Singular Section of a particular 
	Instructor's Office Hours, specified by:
	Instructor, Start Time, End Time, Location, + Relevant Dates.
	"""
	class Meta:
		verbose_name = 'Instructor Office Hour'
		verbose_name_plural = 'Instructor Office Hours'
	
	meetInstructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='iOfficeHours')
	meetStartTime = models.CharField(max_length=7)
	meetEndTime = models.CharField(max_length=7)
	meetLocation = models.CharField(max_length=23)
	meetDates = models.CharField(max_length=7)

	def __str__(self):
		fullOfficeHoursType = "Professor Office Hours:"
		if(self.meetInstructor.iType == "T"):
			fullOfficeHoursType = "Teaching Assistant Office Hours:"
		return str(self.meetInstructor) + " + " + fullOfficeHoursType + " + " + str(self.meetLocation) + " + " + str(self.meetDates) + " + " + str(self.meetStartTime) + " + " + str(self.meetEndTime)
