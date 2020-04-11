from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
	path('courses/',views.CourseAPIView.as_view())
	#URL Path For Updating Office Hours 
	path('update/', views.UpdateOHAPIView.as_view())
]