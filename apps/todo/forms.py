from datetime import date
from django import forms
from django.core.exceptions import ValidationError

from .models import Epic, Task, SubTask

class EpicForm(forms.ModelForm):
    class Meta:
        model = Epic
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        description = cleaned_data.get('description')

        if not title:
            self.add_error("title", "Tiêu đề không được để trống.")
        if not description:
            self.add_error("description", "Mô tả không được để trống.")

        return cleaned_data

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'start_day', 'duration']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'start_day': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        start_day = cleaned_data.get('start_day')
        duration = cleaned_data.get('duration')

        if title and len(title.strip()) < 3:
            self.add_error('title', "Tiêu đề phải có ít nhất 3 ký tự.")

        if duration is not None and duration <= 0:
            self.add_error('duration', "Thời lượng phải lớn hơn 0.")

        if start_day is not None and start_day < date.today():
            self.add_error('start_day', "Ngày bắt đầu không được ở trong quá khứ.")

        return cleaned_data

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
    title = forms.CharField(max_length=200, strip=True, label="Tên nhiệm vụ con")

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title.strip()) < 3:
            raise ValidationError("Tiêu đề phải có ít nhất 3 ký tự.")
        return title