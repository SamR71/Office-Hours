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
    print("logged in user: " + str(request.data.get("user")))
    # Extract username of logged in user
    username = request.data.get("user")
    if username == '':
        return HttpResponse("User not logged in", content_type="text/plain", status=403)

    # Extract details from data in the POST request
    meetInstructor = request.data.get("instructor")
    meetStartTime = request.data.get("startTime")
    meetEndTime = request.data.get("endTime")
    meetLocation = request.data.get("location")
    meetDates = request.data.get("dates")

    # create userScheduleItem
    allExistingUserScheduleItems = userScheduleItem.objects.filter(meetInstructor=meetInstructor).filter(meetStartTime=meetStartTime).filter(meetEndTime=meetEndTime).filter(meetLocation=meetLocation).filter(meetDates=meetDates)
    
    #Initialize User Schedule Item Object To None:
    #Will Be Either Newly Created/Set To Existing Item.
    u = None;
    if(len(allExistingUserScheduleItems) == 0):
        u = userScheduleItem(meetInstructor=meetInstructor, meetStartTime=meetStartTime, meetEndTime=meetEndTime, meetLocation=meetLocation, meetDates=meetDates)
        u.save()
    else:
        u = allExistingUserScheduleItems[0];

    # locate user in the database
    userSchedule = userSchedules.objects.filter(username=username)
    if len(list(userSchedule)) == 0:
        # user does not have entry in database; add entry with empty schedule
        userSchedule = userSchedules(username=username, schedule="")
    else:
        userSchedule = list(userSchedule)[0]
    print(userSchedule)
    # concatenate new course's userScheduleItem to end of user's schedule
    schedule = str(userSchedule)
    if(not(str(u) in str(userSchedule))):
        schedule = str(userSchedule) + "," + str(u)
    print(schedule)
    userSchedule.schedule = schedule 
    userSchedule.save()
    return HttpResponse("Office Hours Added", content_type="text/plain", status=200)

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def getSchedule(request):
    # Extract username of logged in user
    print("logged in user: " + str(request.data.get("user")))
    username = request.data.get("user")
    if username == '':
        return HttpResponse("User not logged in", content_type="text/plain", status=403)

    # Find user's schedule
    userSchedule = userSchedules.objects.filter(username=username)
    if len(list(userSchedule)) == 0:
        # user does not have entry in database; add entry with empty schedule
        userSchedule = userSchedules(username=username, schedule="")
    else:
        userSchedule = list(userSchedule)[0]
    return HttpResponse(str(userSchedule), content_type="text/plain", status=200) # Return user's schedule