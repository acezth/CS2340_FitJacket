from django.urls import path
from . import views

app_name = 'workouts'

urlpatterns = [
    path('', views.index, name='index'),
    path('ai_suggest', views.ai_suggest, name='ai_suggest'),
]