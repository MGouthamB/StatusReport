from django.urls import path

from . import views

urlpatterns = [
    path("login", views.loginUser, name="login"),
    path("employInfo",views.displayEmpInfo,name="employInfo"),
    path("createTask",views.createTask,name="createTask"),
    path("createAccomplishments",views.createAccomplishments,name="createAccomplishments"),
    path("createBlockers",views.createBlockers,name="createBlockers"),
    path("finalSubmit",views.finalSubmit,name="finalSubmit"),
    path("logout",views.logoutUser,name="logout"),
]