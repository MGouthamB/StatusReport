from django.contrib import admin
from .models import Employee,Groups,Tasks
from .forms import EmployeeForm

# Register your models here.
admin.site.register(Tasks)
admin.site.register(Groups)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['user', 'account_type']
    exclude = ['groups']
    form = EmployeeForm

