from django.shortcuts import render, redirect, reverse, get_object_or_404
from public_user.models import Complaint
from django.contrib import messages
from .utils import send_email_to_complaint_approved, send_email_to_complaint_next_steps
from public_user.forms import *
from accounts.forms import UserUpdateForm, ChangeEmailForm
from django.views.generic import View, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LogoutView as BaseLogoutView, PasswordChangeView as BasePasswordChangeView,
    PasswordResetDoneView as BasePasswordResetDoneView, PasswordResetConfirmView as BasePasswordResetConfirmView,
)
from django.conf import settings
from django.utils.crypto import get_random_string
from accounts.models import Activation
from django.contrib.auth import login, authenticate, REDIRECT_FIELD_NAME
from accounts.utils import (
    send_activation_email, send_reset_password_email, send_forgotten_username_email, send_activation_change_email,
)


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


def ministry_incharge_next_update_complaint_form(request, complaint_id):
    complaint = Complaint.objects.get(id=complaint_id)
    print(complaint)
    form = ComplaintNextStepsForms()
    if request.method == "POST":
        form = ComplaintNextStepsForms(request.POST)
        if form.is_valid():
            complaint = Complaint.objects.get(id=complaint_id)
            email_or_start_date = form.cleaned_data['email_or_start_date']
            print(email_or_start_date)
            ministry_name = complaint.ministry_name
            print(ministry_name)
            email = complaint.username.email
            location = complaint.location
            print(location)
            note = complaint.location
            print(note)
            image = complaint.image
            print(image)
            complaint.is_next_update_status = True
            complaint.save()
            send_email_to_complaint_next_steps(complaint, ministry_name, email_or_start_date, email, location, note, image)
            return redirect('complaint_list')
    context = {
        'complaint': complaint,
        'form': form
    }
    return render(request, 'Ministry Incharge/Complaint/complaint_next_steps.html', context=context)


class MinistryChangeEmailView(LoginRequiredMixin, FormView):
    template_name = 'Ministry Incharge/Profile/change_email.html'
    form_class = ChangeEmailForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        initial['email'] = self.request.user.email
        return initial

    def form_valid(self, form):
        user = self.request.user
        email = form.cleaned_data['email']

        if settings.ENABLE_ACTIVATION_AFTER_EMAIL_CHANGE:
            code = get_random_string(20)

            act = Activation()
            act.code = code
            act.user = user
            act.email = email
            act.save()

            send_activation_change_email(self.request, email, code)

            messages.success(self.request, f'To complete the change of email address, click on the link sent to it.')
        else:
            user.email = email
            user.save()

            messages.success(self.request, f'Email successfully changed.')

        return redirect('ministry_change_email')


class MinistryChangeEmailActivateView(View):
    @staticmethod
    def get(request, code):
        act = get_object_or_404(Activation, code=code)

        # Change the email
        user = act.user
        user.email = act.email
        user.save()

        # Remove the activation record
        act.delete()

        messages.success(request, f'You have successfully changed your email!')

        return redirect('ministry_change_email')


class MinistryChangePasswordView(BasePasswordChangeView):
    template_name = 'Ministry Incharge/Profile/change_password.html'

    def form_valid(self, form):
        # Change the password
        user = form.save()

        # Re-authentication
        login(self.request, user)

        messages.success(self.request, f'Your password was changed.')

        return redirect('log_in')


def ministry_incharge_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST or None, request.FILES or None, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated')
            return redirect('ministry_incharge_profile')
    else:
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'u_form': u_form
    }
    return render(request, 'Ministry Incharge/Profile/SuperAdminProfile.html', context)