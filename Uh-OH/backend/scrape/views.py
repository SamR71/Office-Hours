from django.shortcuts import render

from rest_framework import generics
from rest_framework import filters

from .models import Course
from .models import Instructor
from .models import InstructorOfficeHours
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
class InstructorOHAPIView(object):
	"""docstring for UpdateOHAPIView"""
	def __init__(self, arg):
		super(UpdateOHAPIView, self).__init__()
		self.arg = arg
		
	@api_view(['POST'])
	@parser_classes([MultiPartParser, FormParser])
	@csrf_exempt
	def update(request):
		#Get Old InstructorOfficeHours Attributes:
		oldID = request.data.get("oldID")
		#The Other Old Attributes Are As Follows:
		#	oldStartTime, oldEndTime, oldLocation, oldDates.
		#Get New InstructorOfficeHours Attributes:
		newStartTime = request.data.get("newStartTime")
		newEndTime = request.data.get("newEndTime")
		newLocation = request.data.get("newLocation")
		newDates = request.data.get("newDates")
		#Filter + Obtain Old Existing InstructorOfficeHours Object.
		currentOH = InstructorOfficeHours.objects.filter(pk=oldID)
		#Error Checking For Accuracy of Database Filtering:
		if(currentOH != 1):
			return HttpResponse("Error: Specific InstructorOfficeHours Does Not Exist.", content_type="text/plain", status=403)
		#Set New Values To Update Database Object:
		#Dependency on Frontend To Check For Accuracy In Fields:
		currentOH.meetStartTime = newStartTime
		currentOH.meetEndTime = newEndTime
		currentOH.meetLocation = newLocation
		currentOH.meetDates = newDates
		#Note: MeetInstructor Cannot Change.
		#Save Changes To Database Object:
		currentOH.save();
		return HttpResponse("Sucessfully Updated InstructorOfficeHours!", content_type="text/plain", status=200)
		
