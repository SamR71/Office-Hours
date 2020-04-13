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
    repeatpassword = request.data.get("repeatPassword")
    name = request.data.get("fullName")
    # Verify User Has @rpi.edu Email.
    if username[len(username)-8:len(username)] != "@rpi.edu":
        print("not an rpi email\n")
        return Response('Invalid email: Must end in @rpi.edu', status=422)
    #Verify Matching Passwords:
    if password != repeatpassword:
        print("passwords do not match\n")
        return Response('Passwords do not match', status=422)
    #Create User Account + Add To User Database.
    user = User.objects.create_user(username, username, password)
    user.save()
    return HttpResponse("Registration Successful!", content_type="text/plain", status=200)