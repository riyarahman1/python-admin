from django.contrib import admin
from django.urls import path, include
from . import views
import admin1

urlpatterns = [
    path('', views.adminsignin, name="adminsignin"),
    path('userdata/',views.adminhome, name="home"),
    path('update/<int:id>/',views.updateuser, name="updateuser"),
    path('deleteuser/<int:id>/',views.deleteuser, name="deleteuser"),
    path('logoutadmin', views.logoutadmin, name="adminlogoutadmin"),
    path('usersearch/', views.search, name="usersearch"),
    path('Adduser/',views.adduser,name="Adduser"),
    ]
