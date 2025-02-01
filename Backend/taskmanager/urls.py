"""
URL configuration for taskmanager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.shortcuts import redirect
from tasks import views

def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('tasks/')  # Redirect to task list if logged in
    return auth_views.LoginView.as_view()(request)  # Show login page if not logged in

urlpatterns = [
    path('', home_redirect, name='home'),  # Redirect root URL to home_redirect
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout-complete/', views.logout_view, name='logout_complete'),
    path('signup/', views.signup, name='signup'),
    path('tasks/', include('tasks.urls')),
    path('admin/', admin.site.urls),
]
