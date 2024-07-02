from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserForm,CreateTask
from django.contrib import messages
from .models import Projectteams,Tasks


class Memberprojects:
    def __init__(self,request):
        tasks=Projectteams.objects.filter(member=request.user.id).select_related("project")
        projectsdict={}
        self.projects=[]
        for task in tasks:
            if task.project.id not in projectsdict:
                projectsdict[task.project.id]=task.project.name
                self.projects.append({
                    "id":task.project.id,
                    "name":task.project.name
    })

@login_required
def registerUser(request):
    if(request.user.role=="EX"):
        form=CreateTask()
    # return render(request,"logout.html",{"form":form})
        if request.method=="POST":
            form=UserForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("/statusReport/createTask")
            else:
                return HttpResponse(form.errors.as_json())
        return render(request,"register.html",{"form":form})
    else:
        return HttpResponse("No Accesss")

def loginUser(request):
    form=AuthenticationForm()
    if request.method=="POST":
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request,form.get_user())
            obj=Memberprojects(request)
            request.session["projects"]=obj.projects
            return redirect("/statusReport/employInfo")
        else:
            print(form.errors.as_text())
            messages.error(request,form.errors.as_text())
    return render(request,"login.html",{"form":form})

@login_required(login_url="/statusReport/login")
def displayEmpInfo(request):
    return render(request,"members/employInfo.html")

@login_required(login_url="/statusReport/login")
def createTask(request):
    if request.method=="POST":
        # print(request.FILES)
        form=CreateTask(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"Task created successfully")
            return redirect("/statusReport/createTask")
        else:
            print(form.errors.as_text())
            messages.error(request,form.errors.as_text())
    return render(request,"createTask.html",{"projects":request.session["projects"],"user":request.user.id})

@login_required(login_url="/statusReport/login")
def viewTasks(request,*args, **kwargs):
    if request.GET.get("project", default=None):
        print(type(request.GET.get("project", default=None)))
        tasks=Tasks.objects.filter(user=request.user.id,project=int(request.GET.get("project", default=None))).select_related("project")
    else:
        tasks=Tasks.objects.filter(user=request.user.id).select_related("project")
        
    return render(request,"viewTasks.html",{"tasks":tasks,"projects":request.session["projects"]})

@login_required(login_url="/statusReport/login")
def logoutUser(request):
    logout(request)
    return redirect("/statusReport/login")