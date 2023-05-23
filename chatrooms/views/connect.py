from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, TemplateView
from .. import models
from django.contrib.auth.mixins import LoginRequiredMixin


class FollowListView(ListView):
    template_name = 'user/list.html'
    model = models.Connect
    context_object_name = "users_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['title'] = 'フォロー一覧'
        return context


    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs) 
        queryset = queryset.filter(follow_id=self.kwargs.get('pk')).order_by('-created_at')
        qs=[]
        for i in queryset:
            qs.append(i.follower)
        print(qs)
        return qs

class FollowerListView(ListView):
    template_name = 'user/list.html'
    model = models.Connect
    context_object_name = "users_list"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['title'] = 'フォロワー一覧'
        return context

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs) 
        queryset = queryset.filter(follower_id=self.kwargs.get('pk')).order_by('-created_at')
        qs=[]
        for i in queryset:
            qs.append(i.follow)
        print(qs)
        return qs

class ConnectCreateView(CreateView):
    template_name = 'user/connect.html'
    model = models.Connect
    fields = []
    def get_success_url(self):
          pk=self.kwargs['pk']
          return reverse_lazy('ud', kwargs={'pk': pk})
    def form_valid(self, form):
        form.instance.follow = self.request.user
        form.instance.follower = models.CustomUser.objects.get(id=self.kwargs.get('pk'))
        return super(ConnectCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context=super().get_context_data() #元クラスで定義されてるデフォルトのcontextを呼び出してます
        extra={
            'target': models.CustomUser.objects.get(id=self.kwargs.get('pk')),
            'f_or_b': 'フォロー'
        }
        context.update(extra)
        return context
    

class ConnectDeleteView(DeleteView):
    template_name = 'user/connectdel.html'
    model = models.Connect
    
    def post(self,request,**kwargs):
        try:
            connect = models.Connect.objects.get(follower_id=self.kwargs.get('pk'),follow_id=self.request.user.id)
            connect.delete()
        except:
            pass
        return redirect('ul')


    def get_context_data(self, **kwargs):
        context=super().get_context_data() #元クラスで定義されてるデフォルトのcontextを呼び出してます
        extra={
            'target': models.CustomUser.objects.get(id=self.kwargs.get('pk')),
            'f_or_b': 'フォロー'
            }
        context.update(extra)
        return context

    def get_object(self, queryset=None):
        connect = models.Connect.objects.get(follower_id=self.kwargs.get('pk'),follow_id=self.request.user.id)
        return connect

