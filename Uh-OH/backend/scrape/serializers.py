from rest_framework import serializers
from .models import Course, CourseSection, CourseMeetingTime

class MeetingTimeSerializer(serializers.ModelSerializer):
	coursesection_id = serializers.PrimaryKeyRelatedField(queryset=CourseSection.objects.all(),source='meetSection.id')
	class Meta:
		model = CourseMeetingTime
		fields = 	('id',
					'meetSection',
					#'meetType',
					#'meetDates',
					#'meetStartTime',
					#'meetEndTime',
					#'meetInstructor',
					'coursesection_id')

class CourseSectionSerializer(serializers.ModelSerializer):
	course_id = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(),source='currentCourse.id')
	meetingTimes = MeetingTimeSerializer(many=True, read_only=True)
	class Meta:
		model = CourseSection
		fields = ('id', 'currentCourse', 'sectionID', 'course_id', 'meetingTimes')

class CourseSerializer(serializers.ModelSerializer):
	sections = CourseSectionSerializer(many=True, read_only=True)
	class Meta:
		model = Course
		fields = ('id', 'courseName', 'courseValue', 'courseAbbrev', 'sections')
