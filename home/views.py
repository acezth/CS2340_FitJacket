from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views import View

class HomeView(View):
    def get(self, request):
        return render(request, 'home/home.html')