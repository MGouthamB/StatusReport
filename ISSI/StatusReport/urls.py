from django.urls import path

from . import views

urlpatterns = [
    path("login", views.loginUser, name="login"),
    path("register",views.registerUser,name="register"),
    path("createTask",views.createTask,name="create?Task"),
    path("viewTasks",views.viewTasks,name="viewTasks"),
    path("logout",views.logoutUser,name="logout"),
    path("employInfo",views.displayEmpInfo,name="employInfo")
]