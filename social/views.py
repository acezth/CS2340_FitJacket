from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
import requests
from django.utils import timezone
from django.conf import settings
from .models import FriendConnection, ActivityStats
from strava.models import StravaUser, StravaActivity

def refresh_token(strava_user):
    """Refresh Strava access token"""
    refresh_url = "https://www.strava.com/oauth/token"
    data = {
        'client_id': settings.STRAVA_CLIENT_ID,
        'client_secret': settings.STRAVA_CLIENT_SECRET,
        'refresh_token': strava_user.refresh_token,
        'grant_type': 'refresh_token'
    }
    
    response = requests.post(refresh_url, data=data)
    if response.status_code == 200:
        token_data = response.json()
        strava_user.access_token = token_data['access_token']
        strava_user.refresh_token = token_data['refresh_token']
        strava_user.token_expires_at = timezone.now() + timezone.timedelta(seconds=token_data['expires_in'])
        strava_user.save()

def get_strava_friends(strava_user):
    """Fetch user's Strava friends"""
    if not strava_user:
        return []
    
    # Check if token needs refresh
    if strava_user.token_expires_at <= timezone.now():
        refresh_token(strava_user)
    
    # Get Strava friends
    friends_url = "https://www.strava.com/api/v3/athlete/followers"
    headers = {'Authorization': f"Bearer {strava_user.access_token}"}
    response = requests.get(friends_url, headers=headers)
    
    if response.status_code != 200:
        return []
        
    return [friend['id'] for friend in response.json()]

@login_required
def index(request):
    # Get user's friends
    friends = User.objects.filter(
        id__in=request.user.friendships.values_list('friend_id', flat=True)
    )
    
    # Get Strava friends if user has connected Strava
    strava_friends = []
    if hasattr(request.user, 'stravauser'):
        strava_friends = get_strava_friends(request.user.stravauser)
    
    # Get friend suggestions (users with Strava connected who aren't friends)
    suggestions = User.objects.filter(
        Q(stravauser__isnull=False) |  # Users with Strava connected
        Q(stravauser__strava_id__in=strava_friends)  # Your Strava friends
    ).exclude(
        Q(id=request.user.id) |  # Exclude yourself
        Q(id__in=request.user.friendships.values_list('friend_id', flat=True))  # Exclude existing friends
    ).distinct()[:5]
    
    # Update current user's stats
    stats, created = ActivityStats.objects.get_or_create(user=request.user)
    stats.update_stats()
    
    # Get leaderboard data
    distance_leaders = ActivityStats.objects.select_related('user').order_by('-total_distance')[:10]
    elevation_leaders = ActivityStats.objects.select_related('user').order_by('-total_elevation_gain')[:10]
    activity_leaders = ActivityStats.objects.select_related('user').order_by('-total_activities')[:10]
    
    # Get friend activities
    friend_activities = StravaActivity.objects.filter(
        strava_user__user__in=friends
    ).select_related('strava_user__user').order_by('-start_date')[:20]
    
    return render(request, 'social/index.html', {
        'friends': friends,
        'suggestions': suggestions,
        'friend_activities': friend_activities,
        'distance_leaders': distance_leaders,
        'elevation_leaders': elevation_leaders,
        'activity_leaders': activity_leaders,
        'user_stats': stats,
    })

@login_required
def add_friend(request, user_id):
    friend = get_object_or_404(User, id=user_id)
    
    # Don't allow self-friending
    if friend == request.user:
        messages.error(request, "You can't add yourself as a friend!")
        return redirect('social:index')
    
    # Create friendship connection
    FriendConnection.objects.get_or_create(user=request.user, friend=friend)
    messages.success(request, f"You are now friends with {friend.username}!")
    
    return redirect('social:index')

@login_required
def remove_friend(request, user_id):
    friend = get_object_or_404(User, id=user_id)
    FriendConnection.objects.filter(user=request.user, friend=friend).delete()
    messages.success(request, f"Removed {friend.username} from your friends.")
    return redirect('social:index')
