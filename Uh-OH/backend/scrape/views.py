from django.shortcuts import render

from rest_framework import generics
from rest_framework import filters

from .models import Course
from .models import Instructor
from .serializers import CourseSerializer
from .serializers import InstructorSerializer


# Create your views here.
def home(request):
	return render(request, template_name='base.html')

#CourseAPIView Is The View Invoked By The Frontend 
#To Return All Courses Present For The Main Search Page.
class CourseAPIView(generics.ListCreateAPIView):
	search_fields = ['courseName', 'courseAbbrev', 'courseValue']
	filter_backends = (filters.SearchFilter,)
	queryset = Course.objects.all()
	serializer_class = CourseSerializer

#InstructorAPIView Is The View Invoked By The Frontend 
#To Return All Instructors + InstructorOfficeHours Present
#On The Main Homepage.
#This Will Be Used For Updating Office Hours.
class InstructorAPIView(generics.ListCreateAPIView):
	"""docstring for InstructorOfficeHours"""
	search_fields = ['iEmail']
	filter_backends = (filters.SearchFilter,)
	queryset = Instructor.objects.all()
	serializer_class = InstructorSerializer
		
#UpdateOHAPIView Is The View Invoked By The Frontend
#To Update A Specific Office Hours Section.
	#Note: Need To Figure Out How Frontend Is Going To Send 
	#The Office Hours Section They Are Trying To Modify 
	# + The New Data For The Office Hours.
	
		
