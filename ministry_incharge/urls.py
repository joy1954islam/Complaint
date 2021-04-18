from django.urls import path

from ministry_incharge import views

urlpatterns = [
    path('home/', views.ministry_incharge_home, name='ministry_incharge_home'),
    path('complaint/list/', views.complaint_list, name='complaint_list'),

]
