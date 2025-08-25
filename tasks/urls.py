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
    path('auth/signup/', views.SignUpView.as_view(), name='signup'),
    path('auth/login/', views.CustomLoginView.as_view(), name='login'),
    path('auto-logout/', views.auto_logout, name='auto_logout'),
]
