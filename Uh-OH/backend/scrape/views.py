from django.shortcuts import render

from rest_framework import generics
from rest_framework import filters

from .models import Course
from .serializers import CourseSerializer


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

#UpdateOHAPIView Is The View Invoked By The Frontend
#To Update A Specific Office Hours Section.
class UpdateOHAPIView(object):
	"""docstring for UpdateAPIView"""
	#Note: Need To Figure Out How Frontend Is Going To Send 
	#The Office Hours Section They Are Trying To Modify 
	# + The New Data For The Office Hours.
	def __init__(self, arg):
		super(UpdateAPIView, self).__init__()
		self.arg = arg
		
