"""This module handles login operations in the backend"""

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
@csrf_exempt
def userLogin(request):
    """User Login Function/View:"""
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
    """Calls Django Authentication Logout +
    returns Success w/ Empty String To Reset Logged In User In Frontend = ""."""
    logout(request)
    return HttpResponse("", content_type="text/plain", status=200)

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
@csrf_exempt
def userRegister(request):
    # pylint: disable=no-member
    # pylint is incorrectly flagging something as not having a member, even though it does
    """user Registration Function/View"""
    #Extract Email, Password From POST Request Data
    username = request.data.get('email')
    password = request.data.get("password")
    repeatPassword = request.data.get("repeatPassword")
    # Verify User Has @rpi.edu Email.
    if username[len(username)-7:len(username)] != "rpi.edu" or "@" not in username:
        print("Not An RPI Email\n")
        response = "Invalid Email: Must Be An Email Ending in rpi.edu + Must Contain @"
        return HttpResponse(response, content_type="text/plain", status=422)
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
    except User.DoesNotExist:
        user = User.objects.create_user(username, username, password)
        user.save()
        return HttpResponse("Registration Successful!", content_type="text/plain", status=200)
    #User Account Already Exists:
    response = "Error: Registration Unsucessful. Account w/ Same Username Already Exists."
    return HttpResponse(response, content_type="text/plain", status=422)
