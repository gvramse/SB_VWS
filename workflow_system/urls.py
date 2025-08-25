"""
URL configuration for workflow_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from tasks.views import CustomLoginView, SignUpView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tasks.urls')),
    
    # Traditional authentication
    path('auth/login/', CustomLoginView.as_view(), name='login'),
    path('auth/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('auth/signup/', SignUpView.as_view(), name='signup'),
    path('auth/password_change/', auth_views.PasswordChangeView.as_view(
        template_name='registration/password_change.html'
    ), name='password_change'),
    path('auth/password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='registration/password_change_done.html'
    ), name='password_change_done'),
    
    # SSO Authentication URLs
    path('accounts/', include('allauth.urls')),  # Social authentication
    path('oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),  # OAuth2
    path('saml2/', include('djangosaml2.urls')),  # SAML SSO
]
