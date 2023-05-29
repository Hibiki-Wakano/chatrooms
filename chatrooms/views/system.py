from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, TemplateView
from .. import models, forms
from chatrooms.forms import LoginForm, CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime

class NoticeListView(LoginRequiredMixin, ListView):
    template_name = 'system/notice.html'
    model = models.Notice

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset()
        my_notice = queryset.filter(user=self.request.user).order_by('-created_at')[:20]
        my_notice_bin=[]
        for n in my_notice:
            my_notice_bin.append({
                'user': str(n.user),
                'kind': int(n.kind),
                'created_at': str(n.created_at).split('.')[0],
                'text': str(n.text)
            })
        queryset.filter(user=self.request.user).delete()
        return my_notice_bin

class NoticeDelete():
    pass

class ConfigView(LoginRequiredMixin, TemplateView):
    template_name = 'system/config.html'
    def get(self, request, **kwargs):
        ctx = {
            'user': self.request.user,
            'config': models.Config.objects.get(user=self.request.user),
            #'time': self.request.user.created_at-time.time()
        }
        t1=self.request.user.created_at.time()
        t2=datetime.datetime.now()
        print(t1)
        print(t2)
        return self.render_to_response(ctx)





class DevelopmentView(TemplateView):
    template_name = 'system/development.html'
    def get(self, request, **kwargs):
        for user in models.CustomUser.objects.all():
            print(user)
            models.Config.objects.create(
                user = user,
            )
        return redirect('rl')