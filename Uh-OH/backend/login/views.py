from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
# Create your views here.

#User Login Function/View:
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
@csrf_exempt
def userLogin(request):
    #Extract Username, Password From POST Request.
    username = request.data.get("username")
    password = request.data.get("password")
    #Authenticate Credentials Against Django's Built-In User Database.
    user = authenticate(username=username, password=password)
    if user is not None:
        #User Authenticated => Log In.
        login(request, user)
        print("logged in user: " + str(request.user))
        print(request.session)
    else:
        return HttpResponse("Invalid Login", content_type="text/plain", status=401)
    #Return User Login Token To Frontend.
    return HttpResponse(str(request.user), content_type="text/plain", status=200) 

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
@csrf_exempt
def userLogout(request):
    #Calls Django Authentication Logout + Returns Success w/ Empty String To Reset Logged In User In Frontend = "".
    logout(request)
    return HttpResponse("", content_type="text/plain", status=200) 

#Register Users View:
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
@csrf_exempt
def userRegister(request):
    #Extract Email, Password From POST Request Data
    username = request.data.get('email')
    password = request.data.get("password")
    repeatPassword = request.data.get("repeatPassword")
    name = request.data.get("fullName")
    # Verify User Has @rpi.edu Email.
    if username[len(username)-7:len(username)] != "rpi.edu" or "@" not in username:
        print("Not An RPI Email\n")
        return HttpResponse("Invalid Email: Must Be An Email Ending in rpi.edu + Must Contain @", content_type="text/plain", status=422)
    #Verify Matching Passwords:
    if password != repeatPassword:
        print("Passwords Do Not Match\n")
        return Response("Passwords Do Not Match", status=422)
    if len(password) == 0:
        return HttpResponse("Must Specify A Valid Password.", content_type="text/plain", status=422)
    #Create User Account + Add To User Database.
    #Check For Existing User In Django User Objects To Ensure User Is New.
    try:
        user = User.objects.get(username=username)
    except user.DoesNotExist:
        user = User.objects.create_user(username, username, password)
        user.save()
        return HttpResponse("Registration Successful!", content_type="text/plain", status=200)
    #User Account Already Exists:
    return HttpResponse("Error: Registration Unsucessful. Account w/ Same Username Already Exists.", content_type="text/plain", status=422)