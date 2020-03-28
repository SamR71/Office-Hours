from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def addCourse(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    else:
        # User is not logged in
        return HttpResponse("User not logged in", content_type="text/plain", status=403)

def getSchedule(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    else:
        # User is not logged in
        return HttpResponse("User not logged in", content_type="text/plain", status=403)