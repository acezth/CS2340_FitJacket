"""
URL configuration for FitJacket project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from strava import views as strava_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('workouts/', include('workouts.urls')),
    path('social/', include('social.urls')),
    path('logs/', include('logs.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='home/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('strava/connect/', strava_views.strava_connect, name='strava_connect'),
    path('strava/callback/', strava_views.strava_callback, name='strava_callback'),
    path('strava/activities/', strava_views.strava_activities, name='strava_activities'),
]
