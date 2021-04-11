from django.shortcuts import render
from SuperAdmin.models import Ministry
# Create your views here.


def navbar(request):
    ministry = Ministry.obects.all()
    context = {
        'ministry': ministry
    }
    return render(request, 'nav.html', context=context)