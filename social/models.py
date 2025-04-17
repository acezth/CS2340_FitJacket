from django.db import models
from django.contrib.auth.models import User
from strava.models import StravaUser, StravaActivity

# Create your models here.

class FriendConnection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_of')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'friend']
        
    def __str__(self):
        return f"{self.user.username} -> {self.friend.username}"

class ActivityStats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_distance = models.FloatField(default=0)  # in meters
    total_elevation_gain = models.FloatField(default=0)  # in meters
    total_activities = models.IntegerField(default=0)
    total_moving_time = models.IntegerField(default=0)  # in seconds
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Stats"
    
    def update_stats(self):
        """Update user stats based on their Strava activities"""
        if hasattr(self.user, 'stravauser'):
            activities = StravaActivity.objects.filter(strava_user=self.user.stravauser)
            self.total_distance = sum(a.distance for a in activities)
            self.total_elevation_gain = sum(a.total_elevation_gain for a in activities)
            self.total_activities = activities.count()
            self.total_moving_time = sum(a.moving_time for a in activities)
            self.save()
