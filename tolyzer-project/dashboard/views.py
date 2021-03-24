from django.shortcuts import render
from .functions import *
# Create your views here.
def home(request):
    test()
    return render(request, "base.html")