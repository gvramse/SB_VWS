from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Task, Assignee


class AssigneeForm(forms.ModelForm):
    """Form for managing assignee information"""
    class Meta:
        model = Assignee
        fields = ['name', 'email', 'location']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter assignee name...'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter assignee email...'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter assignee location...'
            }),
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'title', 'description', 'status', 'priority',
            'assigned_by', 'assignee_name', 'assignee_email', 'assignee_location',
            'start_date', 'due_date'
        ]
        widgets = {
            'title': forms.Select(attrs={
                'class': 'form-select',
                'id': 'task-title-select'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter task description...'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select'
            }),
            'assigned_by': forms.Select(attrs={
                'class': 'form-select'
            }),
            'assignee_name': forms.Select(attrs={
                'class': 'form-select',
                'id': 'assignee-name-select'
            }),
            'assignee_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'id': 'assignee-email-field',
                'readonly': 'readonly',
                'placeholder': 'Email will auto-populate...'
            }),
            'assignee_location': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'assignee-location-field',
                'readonly': 'readonly',
                'placeholder': 'Location will auto-populate...'
            }),
            'start_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'due_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate assignee choices
        self.fields['assignee_name'].choices = [('', 'Select assignee...')] + [
            (assignee.name, assignee.name) for assignee in Assignee.objects.all()
        ]
        # Populate assigned_by choices with users
        self.fields['assigned_by'].choices = [('', 'Select user...')] + [
            (user.id, f"{user.get_full_name() or user.username}") for user in User.objects.all()
        ]


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user
