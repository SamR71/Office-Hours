from django.urls import path
from . import views

urlpatterns = [
    path('loginuser/<slug:username>/<slug:password>',views.login, name='login'),
    path('registeruser/<slug:name>/<slug:username>/<slug:password>/<slug:repeatpassword>',views.register, name='register')
]