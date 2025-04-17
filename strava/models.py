from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class StravaUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    strava_id = models.BigIntegerField(unique=True)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    token_expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Strava Profile"

class StravaActivity(models.Model):
    strava_user = models.ForeignKey(StravaUser, on_delete=models.CASCADE)
    activity_id = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=255)
    distance = models.FloatField()  # in meters
    moving_time = models.IntegerField()  # in seconds
    elapsed_time = models.IntegerField()  # in seconds
    total_elevation_gain = models.FloatField()  # in meters
    activity_type = models.CharField(max_length=50)
    start_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.start_date}"
