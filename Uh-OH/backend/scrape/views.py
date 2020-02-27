from django.shortcuts import render

from rest_framework import generics
from rest_framework import filters

from .models import Course
from .serializers import CourseSerializer


# Create your views here.
def home(request):
    return render(request, template_name='base.html')

class CourseAPIView(generics.ListCreateAPIView):
    search_fields = ['courseName']
    filter_backends = (filters.SearchFilter,)
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
