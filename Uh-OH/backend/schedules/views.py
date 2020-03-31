from django.shortcuts import render
from django.http import HttpResponse
from .models import userScheduleItem, userSchedules

# Create your views here.
def addCourse(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    else:
        # User is not logged in
        return HttpResponse("User not logged in", content_type="text/plain", status=403)
    meetInstructor = request.data.get("instructor")
    meetStartTime = request.data.get("startTime")
    meetEndTime = request.data.get("endTime")
    meetLocation = request.data.get("location")
    meetDates = request.data.get("dates")

    # create userScheduleItem
    u = userScheduleItem(meetInstructor=meetInstructor, meetStartTime=meetStartTime, meetEndTime=meetEndTime, meetLocation=meetLocation, meetDates=meetDates)
    u.save()

    # locate user in the database
    userSchedule = userSchedules.objects.filter(username=username)
    if userSchedule is None:
        # user does not have entry in database; add entry with empty schedule
        userSchedule = userSchedules(username=username, schedule="")
        
    # concatenate new course's userScheduleItem to end of user's schedule
    schedule = userSchedule + "," + str(u)
    u.schedule = schedule 
    u.save()
    return HttpResponse("Course added", content_type="text/plain", status=200)

def getSchedule(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    else:
        # User is not logged in
        return HttpResponse("User not logged in", content_type="text/plain", status=403)
    userSchedule = userSchedules.objects.filter(username=username)
    if userSchedule is None:
        return HttpResponse("", content_type="text/plain", status=200) # user did not add to their schedule
    return HttpResponse(str(userSchedule), content_type="text/plain", status=200) 