from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Employee,Projects,Tasks,Managers,Projectteams
# from .forms import EmployeeForm

# Register your models here.
# admin.site.register(Employee)
class EmployeeInline(admin.StackedInline):
    model=Employee
    can_delete=False
    verbose_name_plural="employee"

class UserAdmin(UserAdmin):
    inlines=[EmployeeInline]


admin.site.unregister(User)
admin.site.register(User,UserAdmin)
admin.site.register(Tasks)
admin.site.register(Projects)
admin.site.register(Managers)
admin.site.register(Projectteams)

# @admin.register(Employee)
# class EmployeeAdmin(admin.ModelAdmin):
#     list_display = ['user', 'account_type']
#     form = EmployeeForm

