from django import forms
from .models import Employee, Groups

class EmployeeForm(forms.ModelForm):
    selected_groups = forms.ModelMultipleChoiceField(
        queryset=Groups.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Employee
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            selected_ids = list(map(int,self.instance.groups.split(',')))
            self.fields['selected_groups'].initial = Groups.objects.filter(id__in=selected_ids)

    def save(self, commit=True):
        instance = super().save(commit=False)
        selected_groups = self.cleaned_data['selected_groups']
        instance.groups = ','.join(str(group.id) for group in selected_groups)
        if commit:
            instance.save()
        return instance