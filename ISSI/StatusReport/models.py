from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone


# Group table - which stores project teams  in an organization
class Projects(models.Model):
    name = models.CharField(unique=True,max_length=50)
    def __str__(self):
        return self.name


# Tasks table - which  store reports or tasks of a user
class Tasks(models.Model):
    STATUS={
        "completed":"Completed",
        "progress" :"In Progress",
        "start":"YET-TO START"
    }
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project=models.ForeignKey(Projects,on_delete=models.CASCADE)
    startDate = models.DateField(default=timezone.now)
    endDate= models.DateField(default=timezone.now,blank=True)
    taskName = models.TextField(default="CustomTask")
    status = models.TextField(choices=STATUS,default="start")
    accomplishments = models.TextField(blank=True)
    blockers=models.TextField(blank=True)
    document=models.FileField(blank=True)


# Employee table with default user fields and added 2 extra fields
class Employee(models.Model):
    TYPE={
        "FT":"Full Time",
        "PT" :"Part Time",
        "In":"Intern"
    }
    DEPARTMENTS = {
        "ACC": "Accounting",
        "BD": "BD Group",
        "PS": "PS Group",
        "IDC" : "IDC Group",
        "PG":"Products Group",
        "IT":"IT Group"
    }
    ROLE={
        "PM":"Project Manager",
        "GM":"General Manager",
        "HR": "HR Manager",
        "ME":"Member"
    }
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    empType=models.CharField(max_length=4,choices=TYPE,default="FT")
    empDept=models.CharField(max_length=4,choices=DEPARTMENTS,default="IT")
    role = models.CharField(max_length=3, choices=ROLE,default="Member")


class Managers(models.Model):
    manager=models.ForeignKey(User,on_delete=models.CASCADE,related_name="managers")
    member=models.ForeignKey(User,on_delete=models.CASCADE,related_name="members")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["manager","member"],name="unique_manager_member"
            )
        ]

class Projectteams(models.Model):
    project=models.ForeignKey(Projects,on_delete=models.CASCADE)
    member = models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        constraints=[
            models.UniqueConstraint(
                fields=["project","member"],name="unique_project_member"
            )
        ]