from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .. import models
from chatrooms.forms import LoginForm, CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from PIL import Image
from .. import forms

class RoomListView(ListView):
    template_name = 'room/list.html'
    model = models.Room
    context_object_name = "rooms_list"
    def get_queryset(self):
        return models.Room.objects.order_by('-created_at')


class RoomDetailView(DetailView):
    template_name = 'room/detail_.html'
    model = models.Room
    def get_context_data(self, **kwargs):
        context=super().get_context_data() #元クラスで定義されてるデフォルトのcontextを呼び出してます
        extra={'imgurl': "/media/" + str(models.Room.objects.get(id=self.kwargs.get('pk')).image)}
        context.update(extra)
        context['postform'] = forms.PostCreateForm
        print(vars(context['postform']))
        return context


class RoomCreateView(LoginRequiredMixin, CreateView):
    template_name = 'room/create.html'
    model = models.Room
    fields = ['title','image']
    success_url = reverse_lazy('rl')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(RoomCreateView, self).form_valid(form)


class RoomUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'room/update.html'
    model = models.Room
    fields = 'title'
    success_url = reverse_lazy('rl')


class RoomDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'room/delete.html'
    model = models.Room
    success_url = reverse_lazy('rl')

class PostCreate(LoginRequiredMixin, CreateView):
    template_name = 'room/post.html'
    model = models.Post
    form_class = forms.PostCreateForm

    def form_valid(self, form):
        room_pk = self.kwargs.get('pk')
        room = get_object_or_404(models.Room, pk=room_pk)

        post = form.save(commit=False)
        post.room = room
        post.user = self.request.user
        post.save()

        return redirect('rd', pk=room_pk)