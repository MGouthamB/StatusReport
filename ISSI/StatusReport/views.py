from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserForm,CreateTask,CreateAccomplishment,CreateBlockers
from django.contrib import messages
from .models import Projectteams,Tasks,Managers,Accomplishments,Blockers,Documents
from datetime import date
import json


def projectsDict(request):
    projectteams=Projectteams.objects.filter(member=request.user.id).select_related("project")
    projects={}
    for object in projectteams:
        projects[object.project.id]=object.project.name

    return projects
def projectManagers(projects):
    managers=Managers.objects.filter(project__in=list(projects.keys())).select_related("manager")
    managersDict={}
    for i in managers:
        managersDict[i.manager.id]=i.manager.first_name+" "+i.manager.last_name
    return managersDict

def loginUser(request):
    form=AuthenticationForm()
    if request.method=="POST":
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request,form.get_user())
            projects=projectsDict(request)
            managers=projectManagers(projects)
            print(managers)
            request.session["projects"]=projects
            request.session["managers"]=managers
            return redirect("/statusReport/employInfo")
        else:
            print(form.errors.as_text())
            messages.error(request,form.errors.as_text())
    return render(request,"login.html",{"form":form})

@login_required(login_url="/statusReport/login")
def displayEmpInfo(request):
    return render(request,"members/employInfo.html",{"projects":request.session["projects"]})

@login_required(login_url="/statusReport/login")
def createTask(request):
    if request.method=="POST":
        tasks_dict=json.loads(request.body) #converting json bytes data to dict type
        for task in tasks_dict:
            form=CreateTask(tasks_dict[task])
            if form.is_valid():
                form.save()
            else:
                print(form.errors.as_text())
                return HttpResponse(form.errors.as_text())
        return HttpResponse("Successful")
    return render(request,"members/createTask.html",{"projects":request.session["projects"],"token":request.COOKIES['csrftoken'],"userid":request.user.id})

@login_required(login_url="/statusReport/login")
def createAccomplishments(request):
    if request.method=="POST":
        tasks_dict=json.loads(request.body) #converting json bytes data to dict type
        for task in tasks_dict:
            form=CreateAccomplishment(tasks_dict[task])
            if form.is_valid():
                form.save()
            else:
                print(form.errors.as_text())
                return HttpResponse(form.errors.as_text())
        return HttpResponse("Successful")
    return render(request,"members/createAccomplishments.html",{"projects":request.session["projects"],"token":request.COOKIES['csrftoken'],"userid":request.user.id})

@login_required(login_url="/statusReport/login")
def createBlockers(request):
    if request.method=="POST":
        tasks_dict=json.loads(request.body) #converting json bytes data to dict type
        for task in tasks_dict:
            form=CreateBlockers(tasks_dict[task])
            if form.is_valid():
                form.save()
            else:
                print(form.errors.as_text())
                return HttpResponse(form.errors.as_text())
        return HttpResponse("Successful")
    return render(request,"members/createBlockers.html",{"projects":request.session["projects"],"token":request.COOKIES['csrftoken'],"userid":request.user.id})

@login_required(login_url="/statusReport/login")
def finalSubmit(request):
    updatedTaskCount = Tasks.objects.filter(startDate=date.today()).update(editable=False)
    # tasks=Tasks.objects.filter(startDate=date.today())
    # for task in tasks:
    #     print(task.editable)
    updatedAccomplishmentsCount=Accomplishments.objects.filter(startDate=date.today()).update(editable=False)
    updatedBlockersCount=Blockers.objects.filter(startDate=date.today()).update(editable=False)
    return HttpResponse("Succesfull")

@login_required(login_url="/statusReport/login")
def logoutUser(request):
    logout(request)
    return redirect("/statusReport/login")
