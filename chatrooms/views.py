from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from . import models
from .forms import LoginForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView

#INDEX
#   Auth:Login, Logout
#   User:Create, List, Detail, Update, Delete, Mypage
#   Connect:List, Create, Delete
#   Room:Create, List, Detail, Update, Delete, 
#   end

class Login(LoginView):
    form_class = LoginForm
    template_name = 'user/login.html'
class Logout(LoginRequiredMixin, LogoutView):
    pass

class UserListView(ListView):
    template_name = 'user/list.html'
    model = models.CustomUser
    context_object_name = "users_list"
class UserDetailView(DetailView):
    template_name = 'user/detail.html'
    model = models.CustomUser
class UserCreateView(LoginRequiredMixin, CreateView):
    template_name = 'user/create.html'
    model = models.CustomUser
    fields = ['username', 'user_name', 'password', 'memo']
    success_url = reverse_lazy('rl')
class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'user/update.html'
    model = models.CustomUser
    fields = ['username', 'user_name', 'password', 'memo']
    success_url = reverse_lazy('rl')
class UserDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'user/delete.html'
    model = models.CustomUser
    success_url = reverse_lazy('ul')
class Mypage(LoginRequiredMixin, TemplateView):
    template_name = 'user/mypage.html'
    def get(self, request, **kwargs):
        ctx = {
            'user': self.request.user
        }
        return self.render_to_response(ctx)

class FollowListView(ListView):
    pass
class FollowerListView(ListView):
    pass
class ConnectCreateView(CreateView):
    pass
class ConnectDeleteView(DeleteView):
    pass


class RoomListView(ListView):
    template_name = 'room/list.html'
    model = models.Room
    context_object_name = "rooms_list"


class RoomDetailView(DetailView):
    template_name = 'room/detail.html'
    model = models.Room


class RoomCreateView(LoginRequiredMixin, CreateView):
    template_name = 'room/create.html'
    model = models.Room
    fields = ['title','user','image']
    success_url = reverse_lazy('rl')


class RoomUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'room/update.html'
    model = models.Room
    fields = 'title'
    success_url = reverse_lazy('rl')


class RoomDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'room/delete.html'
    model = models.Room
    success_url = reverse_lazy('rl')


class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'room/post.html'
    model = models.Post
    fields = ['text',]
    success_url = reverse_lazy('rl')
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.room = models.Room.objects.get(id=self.kwargs.get('pk'))
        return super(PostCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context=super().get_context_data() #元クラスで定義されてるデフォルトのcontextを呼び出してます
        extra={'room_': models.Room.objects.get(id=self.kwargs.get('pk'))}
        context.update(extra)
        return context