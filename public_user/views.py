from django.shortcuts import render
from SuperAdmin.models import Ministry
from .models import *
from .forms import *
from django.shortcuts import render, redirect, reverse


def create_complaint(request, complaint_id):
    complaint = Ministry.objects.get(id=complaint_id)
    form = ComplaintForms(instance=complaint)
    if request.method == "POST":
        form = ComplaintForms(request.POST or None, request.FILES or None)
        if form.is_valid():
            print('valid form')
            c = form.save(commit=False)
            c.username = request.user
            c.ministry_name = complaint
            c.save()
            return redirect(reverse('home'))
        context = {
            'form': form,
            'complaint': complaint
        }
        return render(request, 'create_complaint.html', context=context)

    if request.method == "GET":
        context = {
            'form': form,
            'complaint': complaint
        }
        return render(request, 'create_complaint.html', context=context)