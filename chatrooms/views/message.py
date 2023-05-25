from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .. import models
from chatrooms.forms import LoginForm, CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from .. import forms

class MessageBoxView(ListView):
    template_name='message/box.html'
    model = models.Message


class MessageRoomView(ListView):
    template_name='message/room.html'
    model = models.Message
    

    def get_queryset(self, **kwargs):
        qs = super().get_queryset()
        try:
            print(self.kwargs.get('p'))
            qs1 = qs.filter(received=self.request.user, sent=models.CustomUser.objects.get(username=self.kwargs.get('p')))
            qs2 = qs.filter(sent=self.request.user, received=models.CustomUser.objects.get(username=self.kwargs.get('p')))
            qs = qs1 | qs2
            qs = qs.order_by("-created_at")
        except:
            qs = []
        print(qs)
        return qs

    def get_context_data(self,**kwargs):
        context = super().get_context_data()
        return context

def ajax():
    pass