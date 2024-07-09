from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from datetime import date

# User table with default User fields and added extra fields
class CustomUser(AbstractUser, PermissionsMixin):
    TYPE = [
        ("FT", "Full Time"),
        ("PT", "Part Time"),
        ("IN", "Intern")
    ]
    DEPARTMENTS = [
        ("ACC", "Accounting"),
        ("BD", "BD Group"),
        ("PS", "PS Group"),
        ("IDC", "IDC Group"),
        ("PG", "Products Group"),
        ("IT", "IT Group")
    ]
    ROLE = [
        ("PM", "Project Manager"),
        ("GM", "General Manager"),
        ("HR", "HR Manager"),
        ("ME", "Member"),
        ("EX", "Executive")
    ]
    email = models.EmailField(unique=True)
    empType = models.CharField(max_length=2, choices=TYPE)
    empDept = models.CharField(max_length=3, choices=DEPARTMENTS)
    role = models.CharField(max_length=2, choices=ROLE)
    USERNAME_FIELD="email"
    REQUIRED_FIELDS = ['first_name', 'last_name', 'empType', 'empDept', 'role',"username"]

# Group table - which stores project teams in an organization
class Projects(models.Model):
    name = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return self.name

# Tasks table - which store reports or tasks of a User
class Tasks(models.Model):
    STATUS = [
        ("completed", "Completed"),
        ("progress", "In Progress"),
        ("start", "YET-TO START")
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    startDate = models.DateField(default=date.today())
    endDate = models.DateField(default=date.today(), blank=True)
    taskName = models.CharField(default="Cusotm Task",max_length=100)
    taskDescription = models.TextField(default="Custom Description")
    status = models.CharField(max_length=10, choices=STATUS, default="start")
    editable=models.BooleanField(default=True)

class Accomplishments(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    startDate = models.DateField(default=date.today())
    endDate = models.DateField(default=date.today(), blank=True)
    accomplishments=models.TextField(default="Custom Accomplishment")
    editable=models.BooleanField(default=True)

class Blockers(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    startDate = models.DateField(default=date.today())
    endDate = models.DateField(default=date.today(), blank=True)
    blockers=models.TextField(default="Custom Blockers")
    editable=models.BooleanField(default=True)

class Documents(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    startDate = models.DateField(default=date.today())
    endDate = models.DateField(default=date.today(), blank=True)
    document=models.TextField("path to file",blank=True)
    editable=models.BooleanField(default=True)

# Managers table
class Managers(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    manager = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["manager", "project"], name="unique_manager_member"
            )
        ]

# Project teams table
class Projectteams(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    member = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["project", "member"], name="unique_project_member"
            )
        ]
