from django.shortcuts import render

# Create your views here.
def index(request):
    """index seite"""
    return render(request, "base.html")