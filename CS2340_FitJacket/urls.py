from django.contrib import admin
from django.urls import path, include
from strava import views as strava_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('workouts/', include('workouts.urls')),
    path('social/', include('social.urls')),
    path('logs/', include('logs.urls')),
    path('strava/connect/', strava_views.strava_connect, name='strava_connect'),
    path('strava/callback/', strava_views.strava_callback, name='strava_callback'),
    path('strava/activities/', strava_views.strava_activities, name='strava_activities'),
] 