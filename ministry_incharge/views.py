from django.shortcuts import render, redirect, reverse
from public_user.models import Complaint
from .utils import send_email_to_complaint_approved


def ministry_incharge_home(request):
    return render(request, 'Ministry Incharge/Home.html')


def complaint_list(request):
    complaint = Complaint.objects.filter(ministry_name=request.user.ministry_name)
    context = {
        'complaint': complaint
    }
    return render(request, 'Ministry Incharge/Complaint/complaint_list.html', context=context)


def ministry_incharge_approved_complaint(request, complaint_id):
    complaint = Complaint.objects.get(id=complaint_id)
    ministry_name = complaint.ministry_name
    email = complaint.username.email
    complaint.is_approved_status = True
    complaint.save()
    send_email_to_complaint_approved(ministry_name, email)
    return redirect('complaint_list')
