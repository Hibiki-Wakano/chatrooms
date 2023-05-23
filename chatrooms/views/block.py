from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView
from .. import models
from django.contrib.auth.mixins import LoginRequiredMixin

class BlockListView(ListView):
    template_name = 'user/list.html'
    model = models.Block
    context_object_name = "users_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['title'] = 'ブロック一覧'
        return context


    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs) 
        queryset = queryset.filter(block=self.request.user).order_by('-created_at')
        qs=[]
        for i in queryset:
            qs.append(i.blocked)
        print(qs)
        return qs

class BlockCreateView(CreateView):
    template_name = 'user/connect.html'
    model = models.Block
    fields = []
    def get_success_url(self):
          return reverse_lazy('ul')
    def form_valid(self, form):
        form.instance.block = self.request.user
        form.instance.blocked = models.CustomUser.objects.get(id=self.kwargs.get('pk'))
        try: 
            connect=models.Connect.objects.get(follower_id=self.kwargs.get('pk'),follow_id=self.request.user.id)
            connect.delete()
        except:
            pass
        try:
            connect=models.Connect.objects.get(follow_id=self.kwargs.get('pk'),follower_id=self.request.user.id)
            connect.delete()
        except:
            pass
        return super(BlockCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context=super().get_context_data() #元クラスで定義されてるデフォルトのcontextを呼び出してます
        extra={
            'target': models.CustomUser.objects.get(id=self.kwargs.get('pk')),
            'f_or_b': 'ブロック'
            }
        context.update(extra)
        return context

class BlockDeleteView(DeleteView):
    template_name = 'user/connectdel.html'
    model = models.Block
    
    def post(self,request,**kwargs):
        try:
            block = models.Block.objects.get(blocked_id=self.kwargs.get('pk'),block_id=self.request.user.id)
            block.delete()
        except:
            pass
        return redirect('ul')


    def get_context_data(self, **kwargs):
        context=super().get_context_data() #元クラスで定義されてるデフォルトのcontextを呼び出してます
        extra={
            'target': models.CustomUser.objects.get(id=self.kwargs.get('pk')),
            'f_or_b': 'ブロック'
            }
        context.update(extra)
        return context

    def get_object(self, queryset=None):
        block = models.Block.objects.get(blocked_id=self.kwargs.get('pk'),block_id=self.request.user.id)
        return block

