from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .. import models
from django.db.models import Q
from chatrooms.forms import LoginForm, CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from .. import forms

class MessageBoxView(ListView):
    template_name='message/box.html'
    model = models.Message

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset()
        
        #自分が送ったか、もしくは自分が受け取ったメッセージのみを取得
        try:
            qs1 = queryset.filter(sent=self.request.user).distinct().values_list('received')
        except:
            qs1 = []
        print('送信人数'+str(qs1.count()))
        try:
            qs2 = queryset.filter(received=self.request.user).distinct().values_list('sent')
        except:
            qs2 = []
        print('受信人数'+str(qs2.count()))
        qs = qs1.union(qs2) #[(id,),(id,),(id,)…]の形式
        new_messages = []
        for q in qs:
            message = models.Message.objects.filter(
                Q(received=self.request.user, sent_id=q[0])|
                Q(sent=self.request.user, received_id=q[0])
                ).last()
            new_messages.append(message)
        new_messages.reverse()
        queryset = new_messages
        print(queryset)
        return queryset


class MessageRoomView(ListView):
    template_name='message/room.html'
    model = models.Message
    

    def get_queryset(self, **kwargs):
        qs = super().get_queryset()
        try:
            qs1 = qs.filter(received=self.request.user, sent=models.CustomUser.objects.get(username=self.kwargs.get('p')))
            qs2 = qs.filter(sent=self.request.user, received=models.CustomUser.objects.get(username=self.kwargs.get('p')))
            qs = qs1 | qs2
            qs = qs.order_by("-created_at")
        except:
            qs = []
        return qs

    def get_context_data(self,**kwargs):
        context = super().get_context_data()
        context['messageform']=forms.MessageCreateForm
        context['p']=self.kwargs.get('p')
        return context

class MessageCreate(LoginRequiredMixin, CreateView):
    template_name = 'message/create.html'
    model = models.Message
    form_class = forms.MessageCreateForm
    
    def form_valid(self, form):
        receive = self.kwargs.get('p')
        received = get_object_or_404(models.CustomUser, username=receive)

        message = form.save(commit=False)
        message.received = received

        message.sent = self.request.user
        message.save()

        return redirect('mr', p=received.username)


def ajax():
    pass

