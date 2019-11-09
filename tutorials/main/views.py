from django.shortcuts import render
from .models import Tutorial


# Create your views here.
def homepage(request):
    tutorials=Tutorial.objects.all()
    return render(request,'main/home.html',{'tutorials':tutorials})