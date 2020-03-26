from django.urls import path

from . import views

urlpatterns = [
    path('add/', views.addCourse, name='addCourse'),
    path('add/', views.getSchedule, name='getSchedule'),
]