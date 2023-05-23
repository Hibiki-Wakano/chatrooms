from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .. import models
from ..forms import CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from PIL import Image

class UserCreateView(LoginRequiredMixin, CreateView):
    template_name = 'user/create.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('rl')

class UserListView(ListView):
    template_name = 'user/list.html'
    model = models.CustomUser
    context_object_name = "users_list"

class UserSearchView(ListView):
    template_name = 'user/list.html'
    model = models.CustomUser
    context_object_name = "users_list"
    def get_context_data(self, **kwargs):
        context=super().get_context_data()
        context['users_list'] = models.CustomUser.objects.filter(username__contains=self.kwargs.get('p'))
        return context

class UserDetailView(DetailView):
    template_name = 'user/detail.html'
    model = models.CustomUser
    def get(self, request, **kwargs):
        if self.request.user.id == self.kwargs.get('pk'):
            return redirect('mp')
        else:
            return super().get(request)

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
    fields = ['user_name', 'memo', 'icon']
    success_url = reverse_lazy('mp')

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
        if self.request.user.icon != 'False':
            img = Image.open("media_local/"+str(self.request.user.icon))
            if img.width!=256 or img.height!=256:
                img_resize = img.resize((256, 256))
                img_resize.save("media_local/"+str(self.request.user.icon))
        return self.render_to_response(ctx)

    def get_context_data(self, **kwargs):
        context=super().get_context_data() #元クラスで定義されてるデフォルトのcontextを呼び出してます
        try: 
            imgurl = models.Connect.objects.get(follower_id=self.kwargs.get('pk'),follow_id=self.request.user.id)
            context['iconurl'] = "/media/" + str(imgurl) 
        except:
            context['iconurl'] = False
        return context