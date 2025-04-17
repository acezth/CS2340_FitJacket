# CS2340_FitJacket
CS2340 Final Project - FitJacket

A fitness tracking application that integrates with Strava to help you track workouts and connect with friends.

## Setup Instructions

1. Clone the repository:
```bash
git clone [repository-url]
cd CS2340_FitJacket
```

2. Create and activate a virtual environment:
```bash
# On macOS/Linux:
python -m venv venv
source venv/bin/activate

# On Windows:
python -m venv venv
.\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply database migrations:
```bash
python manage.py migrate
```

5. Create a superuser (admin) account:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

The application should now be running at `http://localhost:8000`

## Common Issues

### Database Table Not Found

If you see errors like "no such table: strava_stravauser" or similar, it means the database migrations haven't been applied. Run:
```bash
python manage.py migrate
```

### Strava Integration

To use Strava features:
1. Log in to your account
2. Visit the Logs or Social page
3. Click "Connect with Strava"
4. Authorize FitJacket to access your Strava data

## Development

When making database changes:
1. Create migrations: `python manage.py makemigrations`
2. Apply migrations: `python manage.py migrate`
3. Commit both your code changes and the migration files

## Features

- Workout logging
- Strava integration
- Social connections
- Activity tracking
- Leaderboards
