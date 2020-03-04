from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.models import User

# Create your views here.
def login(request, username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponse(status=200)
    else:
        return HttpResponse('Unauthorized', status=401)

def register(request, name, username, password, repeatpassword):
    if username[len(username)-8:len(username)] is not "@rpi.edu":
        return HttpResponse('Unauthorized', status=422)
    if password is not repeatpassword:
        return HttpResponse('Unauthorized', status=422)
    user = User.objects.create_user(name, username, password)
    user.save()
    return HttpResponse(status=200)