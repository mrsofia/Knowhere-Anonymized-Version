from django.urls import path

from . import views

app_name = 'dbui'
urlpatterns = [
    path('', views.index, name='index'),
    path('chronos/', views.chronos, name='chronos'),
    path('chronos/<session_id>/', views.chronos, name='chronos_by_session'),
    path('uploader/', views.upload_file, name='uploader'),
    path('sessions/', views.get_sessions, name='sessions'),
    path('frames/<session_id>/', views.get_frames_by_session, name='frames_by_session'),
]
