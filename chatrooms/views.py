from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from . import models
from .forms import Response
from django.contrib.auth.mixins import LoginRequiredMixin


class RoomsListView(ListView):
    template_name = 'room/list.html'
    model = models.Room
    context_object_name = "rooms_list"


class RoomDetailView(DetailView):
    template_name = 'room/detail.html'
    model = models.Room

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # テンプレートにコメント作成フォームを渡す
        context['response'] = Response
        return context


class RoomCreateView(CreateView):
    template_name = 'room/reate.html'
    model = models.Room
    fields = '__all__'
    success_url = reverse_lazy('rl')


class RoomUpdateView(UpdateView):
    template_name = 'room/update.html'
    model = models.Room
    fields = 'title'
    success_url = reverse_lazy('rl')


class RoomDeleteView(DeleteView):
    template_name = 'room/delete.html'
    model = models.Room
    success_url = reverse_lazy('rl')


class PostCreateView(CreateView):
    template_name = 'room/post.html'
    model = models.Post
    fields = 'text'

    def get_success_url(self):
        return reverse_lazy('rd',kwargs={'pk': self.object.pk})



class UsersListView(ListView):
    template_name = 'user/list.html'
    model = models.CustomUser
    context_object_name = "users_list"


class UsersDetailView(DetailView):
    template_name = 'user/detail.html'
    model = models.CustomUser


class UserCreateView(CreateView):
    template_name = 'user/create.html'
    model = models.CustomUser
    fields = ['username', 'user_name', 'password', 'memo']
    success_url = reverse_lazy('rl')


class UserUpdateView(UpdateView):
    pass


class UserDeleteView(DeleteView):
    pass


class Mypage(TemplateView):
    template_name = 'user/mypage.html'
    def get(self, request, **kwargs):
        ctx = {
            'user': self.request.user
        }
        return self.render_to_response(ctx)