from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserForm
from django.contrib import messages

@login_required
def registerUser(request):
    if(request.user.role=="EX"):
        form = UserForm()
        if request.method=="POST":
            form=UserForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("/statusReport/home")
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
            if(request.user.role=="EX"):
                return redirect("/statusReport/register")
            return redirect("/statusReport/home")
        else:
            messages.error(request,form.errors.as_text())
    return render(request,"login.html",{"form":form})

@login_required(login_url="/statusReport/login")
def home(request):
    return render(request,"logout.html")

def logoutUser(request):
    logout(request)
    return redirect("/statusReport/login")