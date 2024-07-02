from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import  CustomUser,Projects,Tasks,Projectteams
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget, AdminSplitDateTime

# class EmployeeForm(forms.ModelForm):
#     selected_groups = forms.ModelMultipleChoiceField(
#         queryset=Groups.objects.all(),
#         widget=forms.CheckboxSelectMultiple
#     )

#     class Meta:
#         model = Employee
#         fields = "__all__"

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if self.instance and self.instance.pk:
#             selected_ids = list(map(int,self.instance.groups.split(',')))
#             self.fields['selected_groups'].initial = Groups.objects.filter(id__in=selected_ids)

#     def save(self, commit=True):
#         instance = super().save(commit=False)
#         selected_groups = self.cleaned_data['selected_groups']
#         instance.groups = ','.join(str(group.id) for group in selected_groups)
#         if commit:
#             instance.save()
#         return instance

# class Employeeform()

class UserForm(UserCreationForm):
    class Meta:
        model=CustomUser
        fields=["username","email",'first_name', 'last_name', 'empType', 'empDept', 'role']

class CreateTask(forms.ModelForm):
    class Meta:
        model=Tasks
        fields="__all__"