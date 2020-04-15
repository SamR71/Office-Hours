from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
	path('courses/',views.CourseAPIView.as_view()),
	path('hours/', views.InstructorAPIView),
	path('update/', views.InstructorOHAPIView.update, name="InstructorOHAPIView.update")
]