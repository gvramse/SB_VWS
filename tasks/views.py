from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views, logout as auth_logout, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Task, Assignee
from .forms import TaskForm, CustomUserCreationForm, AssigneeForm
import json


def home(request):
    """Home page - show welcome page for all users (authenticated and visitors)"""
    context = {
        'organization_name': 'Samskrita Bharati USA',
        'main_website': 'https://samskritabharatiusa.org/',
        'safl_website': 'https://safl.org/',
        'bookstore_website': 'https://www.sbusapustakapanah.org/',
    }
    return render(request, 'home.html', context)


# User Registration View
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Account created successfully! Please log in.')
        return response


@login_required
def task_list(request):
    """Display user's tasks with search and filter functionality"""
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    tasks = Task.objects.filter(owner=request.user)
    
    if search_query:
        tasks = tasks.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    
    # Pagination
    paginator = Paginator(tasks, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'status_choices': Task.STATUS_CHOICES,
    }
    return render(request, 'tasks/task_list.html', context)


@login_required
def task_detail(request, pk):
    """Display detailed view of a task"""
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    return render(request, 'tasks/task_detail.html', {'task': task})


@login_required
def task_create(request):
    """Create a new task"""
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            # Set assigned_by to current user if not specified
            if not task.assigned_by:
                task.assigned_by = request.user
            task.save()
            messages.success(request, 'Task created successfully!')
            return redirect('task_list')
    else:
        form = TaskForm()
    
    return render(request, 'tasks/task_form.html', {
        'form': form, 
        'title': 'Create New Task'
    })


@login_required
def task_update(request, pk):
    """Update an existing task"""
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'tasks/task_form.html', {
        'form': form, 
        'task': task,
        'title': 'Update Task'
    })


@login_required
def task_delete(request, pk):
    """Delete a task"""
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('task_list')
    
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})


@login_required
@require_POST
def task_status_update(request, pk):
    """AJAX endpoint to update task status"""
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    
    try:
        data = json.loads(request.body)
        new_status = data.get('status')
        
        if new_status in dict(Task.STATUS_CHOICES):
            task.status = new_status
            task.save()
            return JsonResponse({
                'success': True, 
                'message': 'Status updated successfully'
            })
        else:
            return JsonResponse({
                'success': False, 
                'message': 'Invalid status'
            })
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False, 
            'message': 'Invalid JSON data'
        })


@login_required
def dashboard(request):
    """User dashboard with task statistics"""
    user_tasks = Task.objects.filter(owner=request.user)
    
    stats = {
        'total_tasks': user_tasks.count(),
        'pending_tasks': user_tasks.filter(status='pending').count(),
        'in_progress_tasks': user_tasks.filter(status='in_progress').count(),
        'completed_tasks': user_tasks.filter(status='completed').count(),
    }
    
    recent_tasks = user_tasks[:5]
    
    context = {
        'stats': stats,
        'recent_tasks': recent_tasks,
    }
    
    return render(request, 'tasks/dashboard.html', context)


# Assignee Management Views
@login_required
def assignee_list(request):
    """Display list of all assignees"""
    assignees = Assignee.objects.all()
    return render(request, 'tasks/assignee_list.html', {'assignees': assignees})


@login_required
def assignee_create(request):
    """Create a new assignee"""
    if request.method == 'POST':
        form = AssigneeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Assignee created successfully!')
            return redirect('assignee_list')
    else:
        form = AssigneeForm()
    
    return render(request, 'tasks/assignee_form.html', {
        'form': form,
        'title': 'Create New Assignee'
    })


@login_required
def assignee_update(request, pk):
    """Update an existing assignee"""
    assignee = get_object_or_404(Assignee, pk=pk)
    
    if request.method == 'POST':
        form = AssigneeForm(request.POST, instance=assignee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Assignee updated successfully!')
            return redirect('assignee_list')
    else:
        form = AssigneeForm(instance=assignee)
    
    return render(request, 'tasks/assignee_form.html', {
        'form': form,
        'assignee': assignee,
        'title': 'Update Assignee'
    })


@login_required
def assignee_delete(request, pk):
    """Delete an assignee"""
    assignee = get_object_or_404(Assignee, pk=pk)
    
    if request.method == 'POST':
        assignee.delete()
        messages.success(request, 'Assignee deleted successfully!')
        return redirect('assignee_list')
    
    return render(request, 'tasks/assignee_confirm_delete.html', {'assignee': assignee})


@login_required
def get_assignee_info(request):
    """AJAX endpoint to get assignee information for auto-population"""
    assignee_name = request.GET.get('name')
    try:
        assignee = Assignee.objects.get(name=assignee_name)
        return JsonResponse({
            'success': True,
            'email': assignee.email,
            'location': assignee.location
        })
    except Assignee.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Assignee not found'
        })


# Custom login view with signup link
class CustomLoginView(auth_views.LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return '/dashboard/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_signup'] = True
        return context


@csrf_exempt
@require_POST
def auto_logout(request):
    """Handle auto-logout when browser is closed"""
    if request.user.is_authenticated:
        auth_logout(request)
    return JsonResponse({'status': 'logged_out'})