from django.urls import path

from . import views

urlpatterns = [
    path('add/', views.addOH, name='addOH'),
    path('remove/', views.removeOH, name='removeOH'),
    path('get/', views.getSchedule, name='getSchedule'),
    path('update/', views.getSchedule, name='updateSchedules')
]