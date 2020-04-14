from django.shortcuts import render

from rest_framework import generics
from rest_framework import filters

from .models import Course
from .models import Instructor
from .models import InstructorOfficeHours
from .serializers import CourseSerializer
from .serializers import InstructorSerializer
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes

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
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def InstructorAPIView(request):
    #Extract Username of Logged In User.
    print("Logged In User: " + str(request.data.get("user")))
    username = request.data.get("user")
    if(username == ''):
        return HttpResponse("Error: User Not Logged In!", content_type="text/plain", status=403)
    #Extract All Existing Instructor Office Hours:
    allExistingOH = InstructorOfficeHours.objects.filter(meetInstructor__iEmail=username)
    resultOHData = "";
    for k in range(0, len(allExistingOH)):
    	currentOH = allExistingOH[k]
    	resultOHData += str(currentOH)
    	if(k != len(allExistingOH)-1):
    		resultOHData += ", "
    #Return Sucesss:
    return HttpResponse(resultOHData, content_type="text/plain", status=200) # Return user's schedule
		
#UpdateOHAPIView Is The View Invoked By The Frontend
#To Update A Specific Office Hours Section.
	#Note: Need To Figure Out How Frontend Is Going To Send 
	#The Office Hours Section They Are Trying To Modify 
	# + The New Data For The Office Hours.
class InstructorOHAPIView(object):
	"""docstring for UpdateOHAPIView"""
	def __init__(self, arg):
		super(UpdateOHAPIView, self).__init__()
		self.arg = arg
		
	@api_view(['POST'])
	@parser_classes([MultiPartParser, FormParser])
	def update(request):
		#Get Old InstructorOfficeHours Attributes:
		currentID = request.data.get("currentID")
		#The Other Old Attributes Are As Follows:
		#	oldStartTime, oldEndTime, oldLocation, oldDates.
		#Get New InstructorOfficeHours Attributes:
		newStartTime = request.data.get("newStartTime")
		newEndTime = request.data.get("newEndTime")
		newLocation = request.data.get("newLocation")
		newDates = request.data.get("newDates")
		#Filter + Obtain Old Existing InstructorOfficeHours Object.
		print(currentID)
		allExistingOH = InstructorOfficeHours.objects.filter(pk=currentID)
		#Error Checking For Accuracy of Database Filtering:
		if(len(allExistingOH) == 0):
			return HttpResponse("Error: Specific InstructorOfficeHours Does Not Exist!", content_type="text/plain", status=403)
		else:
			if(len(allExistingOH) > 1):
				return HttpResponse("Error: Specific InstructorOfficeHours Exists More Than Once!", content_type="text/plain", status=403)
			currentOH = allExistingOH
			print(currentOH)
			#Set New Values To Update Database Object:
			#Dependency on Frontend To Check For Accuracy In Fields:
			currentOH.meetStartTime = newStartTime
			currentOH.meetEndTime = newEndTime
			currentOH.meetLocation = newLocation
			currentOH.meetDates = newDates
			#Note: MeetInstructor Cannot Change.
			#Save Changes To Database Object:
			print(currentOH)
			currentOH.save();
			return HttpResponse("Sucessfully Updated InstructorOfficeHours!", content_type="text/plain", status=200)
		
