INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'home',
    'workouts',
    'social',
    'logs',
    'strava',
]

# Strava API Configuration
STRAVA_CLIENT_ID = '156138'
STRAVA_CLIENT_SECRET = 'b18f772ef02830f0e9ae1a30fa43cf5ad32c21b8'
STRAVA_REDIRECT_URI = 'http://localhost:8000/strava/callback/' 