from django.urls import path
from . import views
#workouts/urls.py
app_name = 'workouts'

urlpatterns = [
    path('', views.index, name='index'),
    path('ai_suggest', views.ai_suggest, name='ai_suggest'),
]