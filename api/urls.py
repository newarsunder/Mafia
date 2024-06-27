from django.urls import path
from . import views  # Import views from the current directory

urlpatterns = [
    path('get_csrf_token/', views.get_csrf_token, name='get_csrf_token'),
    path('signup/', views.signup, name='signup'),
    path('create_room/', views.create_room, name='create_room'),
    path('get_rooms/', views.get_rooms, name='get_rooms'),
    path('join_room/', views.join_room, name='join_room'),
    path('leave_room/', views.leave_room, name='leave_room'),
]
