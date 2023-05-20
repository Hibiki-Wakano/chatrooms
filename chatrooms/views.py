from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from . import models
from .forms import LoginForm, CustomUserCreationForm
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

class UserCreateView(LoginRequiredMixin, CreateView):
    template_name = 'user/create.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('rl')

class UserListView(ListView):
    template_name = 'user/list.html'
    model = models.CustomUser
    context_object_name = "users_list"
class UserDetailView(DetailView):
    template_name = 'user/detail.html'
    model = models.CustomUser
    def get_context_data(self, **kwargs):
        context=super().get_context_data() #元クラスで定義されてるデフォルトのcontextを呼び出してます
        try: 
            models.Connect.objects.get(follower_id=self.kwargs.get('pk'),follow_id=self.request.user.id)
            context['follow_flag'] = True
        except:
            context['follow_flag'] = False
        try: 
            imgurl=models.CustomUser.objects.get(id=self.kwargs.get('pk')).icon
            if imgurl=='False':
                imgurl="icon/none.png"
            context['imgurl'] = "/media/" + str(imgurl)
        except:
            context['imgurl'] = "/media/icon/none.png"
        return context

class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'user/update.html'
    model = models.CustomUser
    fields = ['username', 'user_name', 'memo', 'icon']
    success_url = reverse_lazy('rl')

    def get_context_data(self, **kwargs):
        context=super().get_context_data()
        print(context)
        return context

class UserDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'user/delete.html'
    model = models.CustomUser
    success_url = reverse_lazy('ul')
class Mypage(LoginRequiredMixin, TemplateView):
    template_name = 'user/mypage.html'
    def get(self, request, **kwargs):
        try: 
            imgurl = self.request.user.icon
            if imgurl=='False':
                imgurl='/media/icon/none.png'
            else:
                imgurl = "/media/" + str(imgurl) 
        except:
            imgurl = "/media/icon/none.png"
        ctx = {
            'user': self.request.user,
            'imgurl' : imgurl
        }
        return self.render_to_response(ctx)

    def get_context_data(self, **kwargs):
        context=super().get_context_data() #元クラスで定義されてるデフォルトのcontextを呼び出してます
        try: 
            imgurl = models.Connect.objects.get(follower_id=self.kwargs.get('pk'),follow_id=self.request.user.id)
            context['iconurl'] = "/media/" + str(imgurl) 
        except:
            context['iconurl'] = False
        return context


class FollowListView(ListView):
    template_name = 'user/follow.html'
    model = models.Connect
    context_object_name = "connect_list"

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs) 
        queryset = queryset.filter(follow_id=self.kwargs.get('pk')).order_by('-created_at')
        return queryset

class FollowerListView(ListView):
    template_name = 'user/follow.html'
    model = models.Connect
    context_object_name = "connect_list"

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs) 
        queryset = queryset.filter(follower_id=self.kwargs.get('pk')).order_by('-created_at')
        return queryset

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
        extra={'follower': models.CustomUser.objects.get(id=self.kwargs.get('pk'))}
        context.update(extra)
        return context
    

def ConnectCreate(request, pk):
    if request.method == 'POST':
        print('ok??')
        object = models.Connect.objects.create(
                follow = request.user,
                follower = models.User.objects.get(pk=pk)
                )
        object.save()
        print('ok?')
        return render(request, 'user/list.html')
    else:
        return render(request, 'user/list.html')

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
        extra={'follower': models.CustomUser.objects.get(id=self.kwargs.get('pk'))}
        context.update(extra)
        return context

    def get_object(self, queryset=None):
        connect = models.Connect.objects.get(follower_id=self.kwargs.get('pk'),follow_id=self.request.user.id)
        return connect



class RoomListView(ListView):
    template_name = 'room/list.html'
    model = models.Room
    context_object_name = "rooms_list"
    def get_queryset(self):
        return models.Room.objects.order_by('-created_at')


class RoomDetailView(DetailView):
    template_name = 'room/detail.html'
    model = models.Room
    def get_context_data(self, **kwargs):
        context=super().get_context_data() #元クラスで定義されてるデフォルトのcontextを呼び出してます
        extra={'imgurl': "/media/" + str(models.Room.objects.get(id=self.kwargs.get('pk')).image)}
        context.update(extra)
        print(context['imgurl'])
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