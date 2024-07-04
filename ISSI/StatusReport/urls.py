from django.urls import path

from . import views

urlpatterns = [
    path("login", views.loginUser, name="login"),
    path("employInfo",views.displayEmpInfo,name="employInfo"),
    path("createTask",views.createTask,name="createTask"),
    path("createAccomplishments",views.createAccomplishments,name="createAccomplishments"),
    path("logout",views.logoutUser,name="logout"),
]