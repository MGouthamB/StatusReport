from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Projects,Tasks,Managers,Projectteams,Accomplishments,Blockers,Documents


class Accountadmin(UserAdmin):
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ("username",'email', 'first_name', 'last_name', 'password1', 'password2',"empType","empDept","role"),
            },
        ),
    )

admin.site.register(CustomUser, Accountadmin)
admin.site.register(Tasks)
admin.site.register(Projects)
admin.site.register(Managers)
admin.site.register(Projectteams)
admin.site.register(Accomplishments)
admin.site.register(Blockers)
admin.site.register(Documents)