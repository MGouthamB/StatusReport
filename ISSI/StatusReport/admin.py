from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Projects,Tasks,Managers,Projectteams


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Tasks)
admin.site.register(Projects)
admin.site.register(Managers)
admin.site.register(Projectteams)

