from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .. import models
from django.db.models import Q
from chatrooms.forms import LoginForm, CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from .. import forms

class NoticeListView(LoginRequiredMixin, ListView):
    template_name = 'system/notice.html'
    model = models.Notice

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset()
        my_notice = queryset.filter(user=self.request.user)
        return queryset
