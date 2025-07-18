from django import forms
from .models import Epic, Task, SubTask

class EpicForm(forms.ModelForm):
    class Meta:
        model = Epic
        fields = ['title', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'start_day', 'duration']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'start_day': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class TaskFormDetail(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'start_day', 'duration', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'start_day': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control custom-select'}),
        }

class SubTaskCreateForm(forms.Form):
    title = forms.CharField(max_length=200, label="Tên nhiệm vụ con")