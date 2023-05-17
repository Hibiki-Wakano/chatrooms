from django.urls import path, include
from . import views
from django.contrib import admin

urlpatterns = [
    path('login', views.Login.as_view(), name='li'),
    path('logout', views.Logout.as_view(), name='lo'),

    path('user/list', views.UserListView.as_view(), name='ul'),
    path('user/<int:pk>', views.UserDetailView.as_view(), name='ud'),
    path('user/create', views.UserCreateView.as_view(), name='uc'),
    path('user/update/<int:pk>', views.UserUpdateView.as_view(), name='uu'),
    path('user/delete/<int:pk>', views.UserDeleteView.as_view(), name='udl'),
    path('mypage', views.Mypage.as_view(), name='mp'),

    path('room/list', views.RoomListView.as_view(), name='rl'),
    path('room/<int:pk>/', views.RoomDetailView.as_view(), name='rd'),
    path('room/create', views.RoomCreateView.as_view(), name='rc'),
    path('room/update/<int:pk>', views.RoomUpdateView.as_view(), name='ru'),
    path('room/delete/<int:pk>', views.RoomDeleteView.as_view(), name='rdl'),

    path('room/<int:pk>/post', views.PostCreateView.as_view(), name='pc'),
]

