from django.shortcuts import render
from django.http import HttpResponse
from .models import UserScheduleItem, UserSchedules
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes

# Create your views here.

#------------------------------------------------------------------------------------------------------------#

#This Function Serves As Handling Adding Office Hours
#To A User's Specific UserSchedule.

#Format addOH For POST Request.
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def addOH(request):
    print("Logged In User: " + str(request.data.get("user")))
    #Extract Username of Logged In User
    username = request.data.get("user")
    if(username == ''):
        return HttpResponse("Error: User Not Logged In!", content_type="text/plain", status=403)

    #Extract Details From Data in the POST Request.
    meetInstructor = request.data.get("instructor")
    meetStartTime = request.data.get("startTime")
    meetEndTime = request.data.get("endTime")
    meetLocation = request.data.get("location")
    meetDates = request.data.get("dates")
    meetCourseName = request.data.get("courseName")
    print(meetCourseName)

    #Create New userScheduleItem.
    allExistingUserScheduleItems = UserScheduleItem.objects.filter(meetCourseName=meetCourseName).filter(meetInstructor=meetInstructor).filter(meetStartTime=meetStartTime).filter(meetEndTime=meetEndTime).filter(meetLocation=meetLocation).filter(meetDates=meetDates)
    #Initialize User Schedule Item Object To None:
    #Will Be Either Newly Created/Set To Existing Item.
    u = None;
    if(len(allExistingUserScheduleItems) == 0):
        u = UserScheduleItem(meetCourseName=meetCourseName, meetInstructor=meetInstructor, meetStartTime=meetStartTime, meetEndTime=meetEndTime, meetLocation=meetLocation, meetDates=meetDates)
        u.save()
    else:
        u = allExistingUserScheduleItems[0];

    #Locate User In The Database.
    userSchedule = UserSchedules.objects.filter(username=username)
    if(len(list(userSchedule)) == 0):
        #User Does Not Have Entry In Database => Add Entry w/ Empty Schedule.
        userSchedule = UserSchedules(username=username, schedule="")
    else:
        #Grab Existing Schedule:
        userSchedule = list(userSchedule)[0]
    print(userSchedule)
    #Concatenate New Course's userScheduleItem To End of User's Schedule.
    schedule = str(userSchedule)
    #Only Append In Case The User Schedule Does Not Already Contain The Current Office Hours.
    if(not(str(u) in str(userSchedule))):
        schedule = str(userSchedule) + "," + str(u)
    else:
        return HttpResponse("Error: You Already Added This To Your Schedule.", content_type="text/plain", status=500)
    print(schedule)
    #Update userSchedule.schedule Attribute:
    userSchedule.schedule = schedule 
    userSchedule.save()
    #Return Success:
    return HttpResponse("Sucessfully Added Office Hours To Schedule!", content_type="text/plain", status=200)

#------------------------------------------------------------------------------------------------------------#

#This Function Serves As Handling Removing Office Hours
#From A User's Specific UserSchedule.

#Format removeOH For POST Request.
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def removeOH(request):
    print("Logged In User: " + str(request.data.get("user")))
    #Extract Username of Logged In User
    username = request.data.get("user")
    if(username == ''):
        return HttpResponse("Error: User Not Logged In!", content_type="text/plain", status=403)

    #Extract Details From Data in the POST Request.
    meetInstructor = request.data.get("instructor")
    meetStartTime = request.data.get("startTime")
    meetEndTime = request.data.get("endTime")
    meetLocation = request.data.get("location")
    meetDates = request.data.get("dates")
    meetCourseName = request.data.get("courseName")
    print(meetCourseName)

    #Create New userScheduleItem.
    allExistingUserScheduleItems = UserScheduleItem.objects.filter(meetCourseName=meetCourseName).filter(meetInstructor=meetInstructor).filter(meetStartTime=meetStartTime).filter(meetEndTime=meetEndTime).filter(meetLocation=meetLocation).filter(meetDates=meetDates)
    #Initialize User Schedule Item Object To None:
    #Will Be Either Newly Created/Set To Existing Item.
    currentOH = None;
    if(len(allExistingUserScheduleItems) == 0):
        return HttpResponse("Error: OfficeHours Does Not Exist In Any User Schedule!", content_type="text/plain", status=403)
    else:
        currentOH = allExistingUserScheduleItems[0];

    #Locate User In The Database.
    userSchedule = UserSchedules.objects.filter(username=username)
    if(len(list(userSchedule)) == 0):
        #User Does Not Have Entry In Database => Add Entry w/ Empty Schedule.
        return HttpResponse("Error: User Has Empty Schedule => Cannot Remove Anything From Empty Schedule.", content_type="text/plain", status=403)
    else:
        #Grab Existing Schedule:
        userSchedule = list(userSchedule)[0]
    print(userSchedule)
    #Concatenate New Course's userScheduleItem To End of User's Schedule.
    schedule = str(userSchedule)
    #Only Append In Case The User Schedule Does Not Already Contain The Current Office Hours.
    if((str(currentOH) in str(userSchedule))):
        searchValue = "," + str(currentOH)
        schedule = str(userSchedule).replace(searchValue, "")
    else:
        return HttpResponse("Error: You Do Not Have This Office Hour Currently Present In Your Schedule.", content_type="text/plain", status=500)
    print(schedule)
    #Update userSchedule.schedule Attribute:
    userSchedule.schedule = schedule 
    userSchedule.save()
    #Return Success:
    return HttpResponse("Sucessfully Removed Office Hours From Schedule!", content_type="text/plain", status=200)

#------------------------------------------------------------------------------------------------------------#

#This Function Serves As Returning The Schedule 
#From The Currently Logged In User.

#Format getSchedule For POST Request.
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def getSchedule(request):
    #Extract Username of Logged In User.
    print("Logged In User: " + str(request.data.get("user")))
    username = request.data.get("user")
    if(username == ''):
        return HttpResponse("Error: User Not Logged In!", content_type="text/plain", status=403)
    #Find User's Schedule:
    userSchedule = UserSchedules.objects.filter(username=username)
    if(len(list(userSchedule)) == 0):
        #User Does Not Have Entry In Database => Add Entry w/ Empty Schedule.
        userSchedule = UserSchedules(username=username, schedule="")
    else:
        #Grab Existing User Schedule:
        userSchedule = list(userSchedule)[0]
    #Return Sucesss:
    return HttpResponse(str(userSchedule), content_type="text/plain", status=200) # Return user's schedule

#------------------------------------------------------------------------------------------------------------#

#This Function Serves As Updating All of User Schedules Present In The Database
#Based On The Frontend Requesting To Update A Particular InstructorOfficeHours.

#Format updateSchedules For POST Request.
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def updateSchedules(request):
    #Load Data From POST Request:
    #Get Old InstructorOfficeHours Attributes:
    currentInstructor = request.data.get("currentInstructor")
    oldStartTime = request.data.get("oldStartTime")
    oldEndTime = request.data.get("oldEndTime")
    oldLocation = request.data.get("oldLocation")
    oldDates = request.data.get("oldDates")
    #Get New InstructorOfficeHours Attributes:
    newStartTime = request.data.get("newStartTime")
    newEndTime = request.data.get("newEndTime")
    newLocation = request.data.get("newLocation")
    newDates = request.data.get("newDates")
    #Filter For Existing User Schedule Items:
    allExistingUserScheduleItems = UserScheduleItem.objects.filter(meetInstructor=currentInstructor).filter(meetStartTime=oldStartTime).filter(meetEndTime=oldEndTime).filter(meetLocation=oldLocation).filter(meetDates=oldDates)
    #Error Checking For No Found Items:
    if(len(allExistingUserScheduleItems) == 0):
        return HttpResponse("Error: UserScheduleItem To Be Updated Itself Does Not Exist!", content_type="text/plain", status=403)
    else:
        currentScheduleItem = allExistingUserScheduleItems[0];
        #Store Previous ScheduleItem STR:
        prevScheduleItemSTR = str(currentScheduleItem)
        #Update Database Object:
        currentScheduleItem.meetStartTime = newStartTime
        currentScheduleItem.meetEndTime = newEndTime
        currentScheduleItem.meetLocation = newLocation
        currentScheduleItem.meetDates = newDates
        currentScheduleItem.save()
        #Store New ScheduleItem STR:
        newScheduleItemSTR = str(currentScheduleItem)
        #Get All User Schedules:
        allUserSchedules = UserSchedules.objects.all();
        for currentUserSchedule in allUserSchedules:        
            #Grab Existing User Schedule:
            if(prevScheduleItemSTR in str(currentUserSchedule)):
                #Update User Schedule Item:
                #Update CurrentUserSchedule w/ New Updated UserScheduleItem. 
                currentUserSchedule.schedule = str(currentUserSchedule).replace(prevScheduleItemSTR, newScheduleItemSTR)
                currentUserSchedule.save()
    #Return Success:
    return HttpResponse("Successfully Updated UserScheduleItem + All UserSchedules!", content_type="text/plain", status=200) 

#------------------------------------------------------------------------------------------------------------#
