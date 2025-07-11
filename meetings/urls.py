from django.urls import path
from . import views

app_name = 'meetings'

urlpatterns = [
    path('', views.meeting_list, name='list'),
    path('my-meetings/', views.my_meetings, name='my_meetings'),
    path('<slug:slug>/', views.meeting_detail, name='detail'),
    path('<slug:slug>/register/', views.register_for_meeting, name='register'),
    path('<slug:slug>/cancel/', views.cancel_meeting_registration, name='cancel'),
]