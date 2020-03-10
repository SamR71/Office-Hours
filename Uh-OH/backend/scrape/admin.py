from django.contrib import admin
from .models import Course, CourseSection, CourseMeetingTime
from .models import Professor, ProfessorOfficeHours
from .models import TeachingAssistant, TeachingAssistantOfficeHours
# Register your models here.
admin.site.register(Course)
admin.site.register(CourseSection)
admin.site.register(CourseMeetingTime)
admin.site.register(Professor)
admin.site.register(ProfessorOfficeHours)
admin.site.register(TeachingAssistant)
admin.site.register(TeachingAssistantOfficeHours)