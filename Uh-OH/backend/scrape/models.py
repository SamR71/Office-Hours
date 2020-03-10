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

class Professor(models.Model):
	"""
	CourseSection Class represents a single section of a Course
	by the Course, sectionID, and instructorName.
	"""
	class Meta:
		verbose_name = 'Professor'
		verbose_name_plural = 'Professors'

	pName = models.CharField(max_length=128)
	pEmail = models.CharField(max_length=128)
	currentCourse = models.ForeignKey(Course, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.currentCourse) + " + " + str(self.pName) + " + " + str(self.pEmail)

class ProfessorOfficeHours(models.Model):
	"""
	CourseSection Class represents a single section of a Course
	by the Course, sectionID, and instructorName.
	"""
	class Meta:
		verbose_name = 'Professor Office Hour'
		verbose_name_plural = 'Professor Office Hours'
        
	meetProfessor = models.ForeignKey(Professor, on_delete=models.CASCADE)
	meetStartTime = models.CharField(max_length=7)
	meetEndTime = models.CharField(max_length=7)
	meetLocation = models.CharField(max_length=23)
	meetDates = models.CharField(max_length=7)

	def __str__(self):
		return str(self.meetProfessor) + " + " + str(self.meetLocation) + " + " + str(self.meetDates) + " + " + str(self.meetStartTime) + " + " + str(self.meetEndTime)

class TeachingAssistant(models.Model):
	"""
	CourseSection Class represents a single section of a Course
	by the Course, sectionID, and instructorName.
	"""
	class Meta:
		verbose_name = 'Teaching Assistant'
		verbose_name_plural = 'Teaching Assistants'

	tName = models.CharField(max_length=128)
	tEmail = models.CharField(max_length=128)
	currentCourse = models.ForeignKey(Course, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.currentCourse) + " + " + str(self.tName) + " + " + str(self.tEmail)

class TeachingAssistantOfficeHours(models.Model):
	"""
	CourseSection Class represents a single section of a Course
	by the Course, sectionID, and instructorName.
	"""
	class Meta:
		verbose_name = 'Teaching Assistant Office Hour'
		verbose_name_plural = 'Teaching Assistant Office Hours'

	meetTA = models.ForeignKey(TeachingAssistant, on_delete=models.CASCADE)
	meetStartTime = models.CharField(max_length=7)
	meetEndTime = models.CharField(max_length=7)
	meetLocation = models.CharField(max_length=23)
	meetDates = models.CharField(max_length=7)

	def __str__(self):
		return str(self.meetTA) + " + " + str(self.meetLocation) + " + " + str(self.meetDates) + " + " + str(self.meetStartTime) + " + " + str(self.meetEndTime)

class CourseSection(models.Model):
	"""
	CourseSection Class represents a single section of a Course
	by the Course, sectionID, and instructorName.
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
	CourseMeetingTime Class represents a specific meeting time 
	of a CourseSection.
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
