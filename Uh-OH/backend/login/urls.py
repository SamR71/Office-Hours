from django.urls import path
from . import views

urlpatterns = [
    path('loginuser/',views.userLogin, name='login'),
    path('logoutuser/', views.userLogout, name='logout'),
    path('registeruser/',views.userRegister, name='register')
]