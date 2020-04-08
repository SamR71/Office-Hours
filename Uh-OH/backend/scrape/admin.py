from django.contrib import admin
from .models import Course, CourseSection, CourseMeetingTime
from .models import Instructor, InstructorOfficeHours

# Register your models here.
#Used To Display Database Models On Admin Page:
admin.site.register(Course)
admin.site.register(CourseSection)
admin.site.register(CourseMeetingTime)
admin.site.register(Instructor)
admin.site.register(InstructorOfficeHours)
