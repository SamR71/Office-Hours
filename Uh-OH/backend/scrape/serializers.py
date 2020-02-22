from rest_framework import serializers
from .models import Course, CourseSection

class CourseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Course
		fields = ('id', 'courseName')

class CourseSectionSerialized(serializers.ModelSerializer):
	class Meta:
		model = CourseSection
		fields = ('id', 'courseName')