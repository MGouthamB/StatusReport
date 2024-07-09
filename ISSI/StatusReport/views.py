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
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
from pathlib import Path


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
    print(managersDict)
    return managersDict

def loginUser(request):
    form=AuthenticationForm()
    if request.method=="POST":
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request,form.get_user())
            projects=projectsDict(request)
            managers=projectManagers(projects)
            request.session["projects"]=projects
            request.session["managers"]=managers
            return redirect("/statusReport/viewTasks")
        else:
            print(form.errors.as_text())
            messages.error(request,form.errors.as_text())
    return render(request,"login.html",{"form":form})

@login_required(login_url="/statusReport/login")
def displayEmpInfo(request):
    return render(request,"members/employInfo.html",{"projects":request.session["projects"],"managers":request.session["managers"]})

@login_required(login_url="/statusReport/login")
def viewTasks(request):
    value=date.today()
    if request.method=="POST":
        value=request.POST["starDate"]
    tasks=Tasks.objects.filter(startDate=value).select_related("project")
    return render(request,"members/viewTasks.html",{"tasks":tasks})

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
def upload_files(request):
    if request.method == 'POST':
        try:
            files = request.FILES.getlist('files')
            file_paths = []
            for file in files:
                fs = FileSystemStorage()
                filename = fs.save(file.name, file)
                file_path = fs.url(filename)
                file_paths.append(filename)

            docs = Documents.objects.get(user=request.user.id)

            print(','.join(file_paths))

            if len(file_paths)>=1:
                print(',' if len(docs.document)>1 else '' + ','.join(file_paths))
                docs.document += ','+ ','.join(file_paths) if len(docs.document)>1 else '' + ','.join(file_paths)
                docs.save()

            return redirect('/statusReport/documents')

        except Exception as e:
            print(e)
            return redirect('/statusReport/documents')

    return render(request, 'login.html')

@login_required(login_url="/statusReport/login")
def documents(request):
    docs = Documents.objects.get(user=request.user.id)
    documents = []
    if docs.document!='':
        for id,doc in enumerate(docs.document.split(',')):
            documents.append({'file_name':doc,'project':'GMS','id':id+1})
    return render(request,"members/documents.html",{"documents":documents})

@login_required(login_url="/statusReport/login")
def delete_document(request):
    try:
        BASE_DIR = Path(__file__).resolve().parent.parent
        docs = Documents.objects.get(user=request.user.id)
        documents = docs.document.split(',')
        file_name = documents[int(request.GET['id'])-1]
        del documents[int(request.GET['id'])-1]
        docs.document = ','.join(documents)
        docs.save()
        os.remove(os.path.join(BASE_DIR,"files\\"+file_name))
        return redirect('/statusReport/documents')

    except Exception as e:
        print(e)
        return redirect('/statusReport/documents')

@login_required(login_url="/statusReport/login")
def submit(request):
    updatedTaskCount = Tasks.objects.filter(startDate=date.today(),editable=True).update(editable=False)
    updatedAccomplishmentsCount=Accomplishments.objects.filter(startDate=date.today(),editable=True).update(editable=False)
    updatedBlockersCount=Blockers.objects.filter(startDate=date.today(),editable=True).update(editable=False)
    return redirect("/statusReport/viewTasks")

@login_required(login_url="/statusReport/login")
def finalSubmit(request):
    return render(request,"members/finalSubmit.html")

@login_required(login_url="/statusReport/login")
def logoutUser(request):
    logout(request)
    return redirect("/statusReport/login")
