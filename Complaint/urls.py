
"""Complaint URL Configuration


The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

"""


from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts import views as account_views
from public_user import views as public_user

urlpatterns = [

    path('home/', account_views.home, name='home'),
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('super/admin/', include('SuperAdmin.urls')),
    path('ministry/incharge/', include('ministry_incharge.urls')),

    path('complaint/<int:complaint_id>/', public_user.create_complaint, name='create_complaint'),

    path('profile/', public_user.public_incharge_profile, name='public_profile'),
    path('change/password/', public_user.PublicChangePasswordView.as_view(), name='public_change_password'),
    path('change/email/', public_user.PublicChangeEmailView.as_view(), name='public_change_email'),
    path('change/email/<code>/', public_user.PublicChangeEmailActivateView.as_view(),
         name='public_change_email_activation'),
    path('ajax/load-police-station/', public_user.load_police, name='ajax_load_police_station'),
    path('my_complaint/', public_user.my_complaint_list, name='my_complaint'),

    path('about/', public_user.about, name='about'),
    path('service/', public_user.service, name='service'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
