from django.shortcuts import render
from public_user.models import Complaint


def ministry_incharge_home(request):
    return render(request, 'Ministry Incharge/Home.html')


def complaint_list(request):
    complaint = Complaint.objects.all()
    context = {
        'complaint': complaint
    }
    return render(request, 'Ministry Incharge/Complaint/complaint_list.html', context=context)

