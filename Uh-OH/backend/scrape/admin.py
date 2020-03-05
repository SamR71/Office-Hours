from django.contrib import admin
from .models import Course, CourseSection, CourseMeetingTime, Professor, ProfessorOfficeHours
# Register your models here.
admin.site.register(Course)
admin.site.register(CourseSection)
admin.site.register(CourseMeetingTime)
admin.site.register(Professor)
admin.site.register(ProfessorOfficeHours)