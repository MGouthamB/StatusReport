from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils import timezone

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
    REQUIRED_FIELDS = ['first_name', 'last_name', 'empType', 'empDept', 'role']

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
    startDate = models.DateField(default=timezone.now)
    endDate = models.DateField(default=timezone.now, blank=True)
    taskName = models.TextField(default="CustomTask")
    status = models.CharField(max_length=10, choices=STATUS, default="start")
    accomplishments = models.TextField(blank=True)
    blockers = models.TextField(blank=True)
    document = models.FileField(blank=True)

# Managers table
class Managers(models.Model):
    manager = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="managers")
    member = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="members")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["manager", "member"], name="unique_manager_member"
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
