from django.shortcuts import render
from strava.models import StravaActivity

def index(request):
    strava_activities = []
    if hasattr(request.user, 'stravauser'):
        strava_activities = StravaActivity.objects.filter(
            strava_user=request.user.stravauser
        ).order_by('-start_date')
    
    return render(request, 'logs/index.html', {
        'strava_activities': strava_activities
    })
