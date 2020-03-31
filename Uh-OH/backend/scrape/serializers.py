from rest_framework import serializers
from .models import Course, CourseSection, CourseMeetingTime
from .models import Instructor, InstructorOfficeHours

class CourseMeetingTimeSerializer(serializers.ModelSerializer):
	coursesection_id = serializers.PrimaryKeyRelatedField(queryset=CourseSection.objects.all(), source='meetSection.id')
	class Meta:
		model = CourseMeetingTime
		fields = 	('id',
					'meetSection',
					'meetType',
					'meetDates',
					'meetStartTime',
					'meetEndTime',
					'meetInstructor',
					'coursesection_id')

class CourseSectionSerializer(serializers.ModelSerializer):
	course_id = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), source='currentCourse.id')
	courseMeetingTimes = CourseMeetingTimeSerializer(many=True, read_only=True)
	class Meta:
		model = CourseSection
		fields = ('id', 'currentCourse', 'sectionID', 'course_id', 'courseMeetingTimes')

#Initial Untested Serializer For InstructorOfficeHours:
#Tried To Follow Existing Format/Syntax As Above Serializers.
#Note To Team: Frontend Would Have To Grab iType From meetInstructor 
#To Determine/Output Whether ProfessorOfficeHours/TeachingAssistantOfficeHours.
class InstructorOfficeHoursSerializer(serializers.ModelSerializer):
	instructor_id = serializers.PrimaryKeyRelatedField(queryset=Instructor.objects.all(), source='meetInstructor.id')
	class Meta:
		model = InstructorOfficeHours
		fields = 	('id',
					'meetInstructor',
					'meetLocation',
					'meetDates',
					'meetStartTime',
					'meetEndTime',
					'instructor_id')

#Initial Untested Serializer For Instructor:
#Tried To Follow Existing Format/Syntax As Above Serializers.
#Note To Team: Frontend Would Have To Grab iType From This Object 
#To Determine/Output Whether Professor/TeachingAssistant.
class InstructorSerializer(serializers.ModelSerializer):
	#Adjust For Instructor Parameters:
	course_id = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), source='currentCourse.id')
	iOfficeHours = InstructorOfficeHoursSerializer(many=True, read_only=True)
	class Meta:
		model = Instructor
		fields = ('id', 'currentCourse', 'iType', 'iName', 'iEmail', 'course_id', 'iOfficeHours')

#Note To Team: Added Field For Instructors. 
class CourseSerializer(serializers.ModelSerializer):
	sections = CourseSectionSerializer(many=True, read_only=True)
	instructors = InstructorSerializer(many=True, read_only=True)
	class Meta:
		model = Course
		fields = ('id', 'courseName', 'courseValue', 'courseAbbrev', 'sections', 'instructors')
