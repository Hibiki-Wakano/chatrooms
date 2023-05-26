from django.urls import path, include
from .views import auth,user,notice,connect,block,message,room

from django.contrib import admin

urlpatterns = [
    path('login', auth.Login.as_view(), name='li'),
    path('logout', auth.Logout.as_view(), name='lo'),

    path('notice', notice.NoticeListView.as_view(), name='nl'),



    path('user/list', user.UserListView.as_view(), name='ul'),
    path('user/search/<p>', user.UserSearchView.as_view(), name='us'),
    path('user/<int:pk>', user.UserDetailView.as_view(), name='ud'),
    path('user/create', user.UserCreateView.as_view(), name='uc'),
    path('user/<int:pk>/update', user.UserUpdateView.as_view(), name='uu'),
    path('user/<int:pk>/delete', user.UserDeleteView.as_view(), name='udl'),
    path('mypage', user.Mypage.as_view(), name='mp'),
    path('blocklist',block.BlockListView.as_view(), name='bl'),
    path('user/<int:pk>/block', block.BlockCreateView.as_view(), name='bc'),
    path('user/<int:pk>/blockend', block.BlockDeleteView.as_view(), name='bd'),
    path('user/<int:pk>/follow',connect.FollowListView.as_view(), name='fl1'),
    path('user/<int:pk>/follower',connect.FollowerListView.as_view(), name='fl2'),
    path('user/<int:pk>/connect',connect.ConnectCreateView.as_view(), name='cc'),
    path('user/<int:pk>/disconnect',connect.ConnectDeleteView.as_view(), name='cd'),
    path('messagebox',message.MessageBoxView.as_view(), name="mb"),
    path('message/<p>',message.MessageRoomView.as_view(), name="mr"),
    path('message/create/<p>',message.MessageCreate.as_view(), name="mc"),
    path('message/ajax',message.ajax, name="majax"),


    path('room/list', room.RoomListView.as_view(), name='rl'),
    path('room/<int:pk>/', room.RoomDetailView.as_view(), name='rd'),
    path('room/create', room.RoomCreateView.as_view(), name='rc'),
    path('room/<int:pk>/update', room.RoomUpdateView.as_view(), name='ru'),
    path('room/<int:pk>/delete', room.RoomDeleteView.as_view(), name='rdl'),

    path('room/<int:pk>/komento', room.PostCreate.as_view(), name='pc'),#ok
    path('', room.RoomListView.as_view(), name='index'),
]

