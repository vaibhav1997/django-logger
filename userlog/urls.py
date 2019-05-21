from django.urls import path, include
from django.conf.urls import url
from . import views



urlpatterns = [
    path('', views.index, name="index"),
    path('userlogin', views.userlogin, name="user-login"),
    path('userlogout', views.userlogout, name="user-logout"),
    path('activate', views.activate, name="activate-api"),
    path('ring', views.ring, name="ring-api"),
]