from django.shortcuts import render
from SuperAdmin.models import Ministry
from .models import *
from .forms import *
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
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
from django.contrib import messages


@login_required(login_url='log_in')
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

    if request.method == "GET":
        context = {
            'form': form,
            'complaint': complaint
        }
        return render(request, 'create_complaint.html', context=context)


def about(request):
    return render(request, 'about.html')


def service(request):
    return render(request, 'service.html')


class PublicChangeEmailView(LoginRequiredMixin, FormView):
    template_name = 'change_email.html'
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

        return redirect('public_change_email')


class PublicChangeEmailActivateView(View):
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

        return redirect('public_change_email')


class PublicChangePasswordView(BasePasswordChangeView):
    template_name = 'change_password.html'

    def form_valid(self, form):
        # Change the password
        user = form.save()

        # Re-authentication
        login(self.request, user)

        messages.success(self.request, f'Your password was changed.')

        return redirect('log_in')


def public_incharge_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST or None, request.FILES or None, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated')
            return redirect('public_profile')
    else:
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'u_form': u_form
    }
    return render(request, 'PublicProfile.html', context)