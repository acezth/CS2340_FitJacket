from django.urls import path
from . import views

app_name = 'social'

urlpatterns = [
    path('', views.index, name='index'),
    path('friend/add/<int:user_id>/', views.add_friend, name='add_friend'),
    path('friend/remove/<int:user_id>/', views.remove_friend, name='remove_friend'),
]