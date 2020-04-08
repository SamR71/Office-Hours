from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
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
@csrf_exempt
def userLogin(request):
    # Extract user name and password from POST request
    username = request.data.get("username")
    password = request.data.get("password")
    # Authenticate credentials against Django's built-in user database
    user = authenticate(username=username, password=password)
    if user is not None:
        # User authenticated, log in
        login(request, user)
        print("logged in user: " + str(request.user))
        print(request.session)
    else:
        return HttpResponse("Invalid Login", content_type="text/plain", status=401)
    return HttpResponse(str(request.user), content_type="text/plain", status=200) # Return user login token to the frontend

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
@csrf_exempt
def userRegister(request):
    # Extract email and password from POST request data
    username = request.data.get('email')
    password = request.data.get("password")
    repeatpassword = request.data.get("repeatPassword")
    name = request.data.get("fullName")
    # Verify that user has an @rpi.edu email
    if username[len(username)-8:len(username)] != "@rpi.edu":
        print("not an rpi email\n")
        return Response('Invalid email: Must end in @rpi.edu', status=422)
    # Verify that passwords match
    if password != repeatpassword:
        print("passwords do not match\n")
        return Response('Passwords do not match', status=422)
    # Create user account and add it to the user database
    user = User.objects.create_user(username, username, password)
    user.save()
    return HttpResponse("Registration Successful!", content_type="text/plain", status=200)