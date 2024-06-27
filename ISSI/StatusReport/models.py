from django.db import models
from django.contrib.auth.models import User
from datetime import date


# Group table - which stores project teams  in an organization
class Groups(models.Model):
    name = models.CharField(unique=True,max_length=50)

    def __str__(self):
        return self.name


# Tasks table - which  store reports or tasks of a user
class Tasks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField()
    date = models.DateField(default=date.today())
    completed = models.BooleanField(default=False)

    # class Meta:
    #     permissions=(
    #         ("view_all_reports","can view reports of all the users"),
    #         ("view_project_reports","can view reports of all users for a particular project")
    #     )


# Employee table with default user fields and added 2 extra fields
class Employee(models.Model):
    ACCOUNT_TYPES = {
        "SA": "System Administrator",
        "PM": "Project Manager",
        "M": "Project Member"
    }
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    groups = models.TextField(blank=True)
    account_type = models.CharField(max_length=3, choices=ACCOUNT_TYPES, default="M")
