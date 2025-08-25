from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/create/', views.task_create, name='task_create'),
    path('tasks/<int:pk>/', views.task_detail, name='task_detail'),
    path('tasks/<int:pk>/edit/', views.task_update, name='task_update'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('tasks/<int:pk>/status/', views.task_status_update, name='task_status_update'),
    
    # Assignee Management URLs
    path('assignees/', views.assignee_list, name='assignee_list'),
    path('assignees/create/', views.assignee_create, name='assignee_create'),
    path('assignees/<int:pk>/edit/', views.assignee_update, name='assignee_update'),
    path('assignees/<int:pk>/delete/', views.assignee_delete, name='assignee_delete'),
    path('assignees/bulk-upload/', views.bulk_assignee_upload, name='bulk_assignee_upload'),
    path('assignees/get-info/', views.get_assignee_info, name='get_assignee_info'),
    
    path('auth/signup/', views.SignUpView.as_view(), name='signup'),
    path('auth/login/', views.CustomLoginView.as_view(), name='login'),
    path('auto-logout/', views.auto_logout, name='auto_logout'),
]
