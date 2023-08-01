from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('signup/', views.register, name='signup'),
    path('login/', views.Login, name='login'),
    path('otp/', views.otp, name='otp'),
    path('convo/', views.convo , name='convo'),
    path('send', views.send, name='send'),
    path('getMessages/', views.getMessages, name='getMessages'),
    path('logout/', views.Logout, name='logout'),
]