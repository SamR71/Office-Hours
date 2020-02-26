from rest_framework import serializers
from .models import Course, CourseSection

class CourseSectionSerializer(serializers.ModelSerializer):
	course_id = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(),source='currentCourse.id')
	class Meta:
		model = CourseSection
		fields = ('id', 'currentCourse', 'course_id')

class CourseSerializer(serializers.ModelSerializer):
	sections = CourseSectionSerializer(many=True, read_only=True)
	class Meta:
		model = Course
		fields = ('id', 'courseName', 'sections')
