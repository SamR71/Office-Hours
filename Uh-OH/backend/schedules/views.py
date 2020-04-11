from django.shortcuts import render
from django.http import HttpResponse
from .models import userScheduleItem, userSchedules
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes

# Create your views here.
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def addCourse(request):
    print("Logged In User: " + str(request.data.get("user")))
    #Extract Username of Logged In User
    username = request.data.get("user")
    if username == '':
        return HttpResponse("Error: User Not Logged In!", content_type="text/plain", status=403)

    #Extract Details From Data in the POST Request.
    meetInstructor = request.data.get("instructor")
    meetStartTime = request.data.get("startTime")
    meetEndTime = request.data.get("endTime")
    meetLocation = request.data.get("location")
    meetDates = request.data.get("dates")

    #Create New userScheduleItem.
    allExistingUserScheduleItems = userScheduleItem.objects.filter(meetInstructor=meetInstructor).filter(meetStartTime=meetStartTime).filter(meetEndTime=meetEndTime).filter(meetLocation=meetLocation).filter(meetDates=meetDates)
    #Initialize User Schedule Item Object To None:
    #Will Be Either Newly Created/Set To Existing Item.
    u = None;
    if(len(allExistingUserScheduleItems) == 0):
        u = userScheduleItem(meetInstructor=meetInstructor, meetStartTime=meetStartTime, meetEndTime=meetEndTime, meetLocation=meetLocation, meetDates=meetDates)
        u.save()
    else:
        u = allExistingUserScheduleItems[0];

    #Locate User In The Database.
    userSchedule = userSchedules.objects.filter(username=username)
    if len(list(userSchedule)) == 0:
        #User Does Not Have Entry In Database => Add Entry w/ Empty Schedule.
        userSchedule = userSchedules(username=username, schedule="")
    else:
        #Grab Existing Schedule:
        userSchedule = list(userSchedule)[0]
    print(userSchedule)
    #Concatenate New Course's userScheduleItem To End of User's Schedule.
    schedule = str(userSchedule)
    #Only Append In Case The User Schedule Does Not Already Contain The Current Office Hours.
    if(not(str(u) in str(userSchedule))):
        schedule = str(userSchedule) + "," + str(u)
    print(schedule)
    #Update userSchedule.schedule Attribute:
    userSchedule.schedule = schedule 
    userSchedule.save()
    #Return Success:
    return HttpResponse("Sucessfully Added Office Hours To Schedule!", content_type="text/plain", status=200)

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def getSchedule(request):
    #Extract Username of Logged In User.
    print("Logged In User: " + str(request.data.get("user")))
    username = request.data.get("user")
    if username == '':
        return HttpResponse("Error: User Not Logged In!", content_type="text/plain", status=403)
    #Find User's Schedule:
    userSchedule = userSchedules.objects.filter(username=username)
    if len(list(userSchedule)) == 0:
        #User Does Not Have Entry In Database => Add Entry w/ Empty Schedule.
        userSchedule = userSchedules(username=username, schedule="")
    else:
        #Grab Existing User Schedule:
        userSchedule = list(userSchedule)[0]
    #Return Sucesss:
    return HttpResponse(str(userSchedule), content_type="text/plain", status=200) # Return user's schedule

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def updateSchedules(request):
    #Extract Username of Logged In User.
    print("Logged In User: " + str(request.data.get("user")))
    username = request.data.get("user")
    #Current User Does Not Exist/Not Logged In.
    if username == '':
        #Return Failure:
        return HttpResponse("Error: User Not Logged In!", content_type="text/plain", status=403)
    #Return Success:
    return HttpResponse("Successfully Update Schedule!", content_type="text/plain", status=200) 
    