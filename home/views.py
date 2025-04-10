from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views import View

# Create your views here.
class HomeView(View):
    def get(self, request):
        return render(request, 'home/home.html')

def home(request):
    return render(request, 'home/home.html')

def workouts(request):
    return render(request, 'home/workouts.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'home/register.html', {'form': form})