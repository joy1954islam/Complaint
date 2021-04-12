from django.shortcuts import render

# Create your views here.


def ministry_incharge_home(request):
    return render(request, 'Ministry Incharge/Home.html')

