from django.urls import path

from . import views

urlpatterns = [
    path("login", views.loginUser, name="login"),
    path("employInfo",views.displayEmpInfo,name="employInfo"),
    path("viewTasks",views.viewTasks,name="viewTasks"),
    path("createTask",views.createTask,name="createTask"),
    path("createAccomplishments",views.createAccomplishments,name="createAccomplishments"),
    path("createBlockers",views.createBlockers,name="createBlockers"),
    path("upload_documents", views.upload_files, name="Upload docs"),
    path("documents", views.documents, name="docs page"),
    path("delete_document", views.delete_document, name="delete doc"),
    path("finalSubmit",views.finalSubmit,name="finalSubmit"),
    path("submit",views.submit,name="submit"),
    path("logout",views.logoutUser,name="logout"),
]