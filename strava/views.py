from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.utils import timezone
import requests
from datetime import datetime, timedelta
from .models import StravaUser, StravaActivity

STRAVA_CLIENT_ID = settings.STRAVA_CLIENT_ID
STRAVA_CLIENT_SECRET = settings.STRAVA_CLIENT_SECRET
STRAVA_REDIRECT_URI = settings.STRAVA_REDIRECT_URI

@login_required
def strava_connect(request):
    """Redirect user to Strava authorization page"""
    auth_url = (
        f"https://www.strava.com/oauth/authorize?"
        f"client_id={STRAVA_CLIENT_ID}&"
        f"redirect_uri={STRAVA_REDIRECT_URI}&"
        f"response_type=code&"
        f"scope=activity:read_all"
    )
    return redirect(auth_url)

@login_required
def strava_callback(request):
    """Handle Strava OAuth callback"""
    code = request.GET.get('code')
    if not code:
        messages.error(request, "Authorization failed. Please try again.")
        return redirect('home')

    # Exchange code for access token
    token_url = "https://www.strava.com/oauth/token"
    data = {
        'client_id': STRAVA_CLIENT_ID,
        'client_secret': STRAVA_CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code'
    }
    
    response = requests.post(token_url, data=data)
    if response.status_code != 200:
        messages.error(request, "Failed to connect to Strava. Please try again.")
        return redirect('home')

    token_data = response.json()
    
    # Get athlete data
    athlete_url = "https://www.strava.com/api/v3/athlete"
    headers = {'Authorization': f"Bearer {token_data['access_token']}"}
    athlete_response = requests.get(athlete_url, headers=headers)
    
    if athlete_response.status_code != 200:
        messages.error(request, "Failed to fetch Strava profile. Please try again.")
        return redirect('home')

    athlete_data = athlete_response.json()
    
    # Create or update StravaUser
    strava_user, created = StravaUser.objects.update_or_create(
        user=request.user,
        defaults={
            'strava_id': athlete_data['id'],
            'access_token': token_data['access_token'],
            'refresh_token': token_data['refresh_token'],
            'token_expires_at': timezone.now() + timedelta(seconds=token_data['expires_in'])
        }
    )

    messages.success(request, "Successfully connected to Strava!")
    return redirect('strava_activities')

@login_required
def strava_activities(request):
    """Fetch and display Strava activities"""
    try:
        strava_user = StravaUser.objects.get(user=request.user)
    except StravaUser.DoesNotExist:
        messages.error(request, "Please connect your Strava account first.")
        return redirect('strava_connect')

    # Check if token needs refresh
    if timezone.now() >= strava_user.token_expires_at:
        refresh_token(strava_user)

    # Fetch activities
    activities_url = "https://www.strava.com/api/v3/athlete/activities"
    headers = {'Authorization': f"Bearer {strava_user.access_token}"}
    response = requests.get(activities_url, headers=headers)

    if response.status_code != 200:
        messages.error(request, "Failed to fetch activities. Please try again.")
        return redirect('home')

    activities = response.json()
    
    # Store activities in database
    for activity in activities:
        StravaActivity.objects.update_or_create(
            activity_id=activity['id'],
            defaults={
                'strava_user': strava_user,
                'name': activity['name'],
                'distance': activity['distance'],
                'moving_time': activity['moving_time'],
                'elapsed_time': activity['elapsed_time'],
                'total_elevation_gain': activity['total_elevation_gain'],
                'activity_type': activity['type'],
                'start_date': datetime.fromisoformat(activity['start_date'].replace('Z', '+00:00'))
            }
        )

    # Get activities from database
    user_activities = StravaActivity.objects.filter(strava_user=strava_user).order_by('-start_date')
    
    return render(request, 'strava/activities.html', {
        'activities': user_activities
    })

def refresh_token(strava_user):
    """Refresh Strava access token"""
    refresh_url = "https://www.strava.com/oauth/token"
    data = {
        'client_id': STRAVA_CLIENT_ID,
        'client_secret': STRAVA_CLIENT_SECRET,
        'refresh_token': strava_user.refresh_token,
        'grant_type': 'refresh_token'
    }
    
    response = requests.post(refresh_url, data=data)
    if response.status_code == 200:
        token_data = response.json()
        strava_user.access_token = token_data['access_token']
        strava_user.refresh_token = token_data['refresh_token']
        strava_user.token_expires_at = timezone.now() + timedelta(seconds=token_data['expires_in'])
        strava_user.save()
