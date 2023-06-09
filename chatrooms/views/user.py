from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .. import models
from ..forms import CustomUserCreationForm, CustomUserSearchForm
from . import mixins
from django.contrib.auth.mixins import LoginRequiredMixin
from PIL import Image

class UserCreateView(CreateView):
    template_name = 'user/create.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('rl')

class UserListView(ListView):
    template_name = 'user/list.html'
    model = models.CustomUser
    context_object_name = "users_list"
    def get_queryset(self, **kwargs):
        qs=super().get_queryset(**kwargs)
        for u in qs:
            try:
                models.Block.objects.get(block_id=self.request.user.pk, blocked_id=u.pk)
                print('I blocked '+str(u.username))
                qs = qs.exclude(id=u.pk)
            except:
                pass
            try:
                models.Block.objects.get(blocked_id=self.request.user.pk, block_id=u.pk)
                print(str(u.username)+' blocked me')
                qs = qs.exclude(id=u.pk)
            except:
                pass
        return qs



    def get_context_data(self, **kwargs):
        context=super().get_context_data()
        return context

class UserSearchView(ListView):
    template_name = 'user/list.html'
    model = models.CustomUser
    context_object_name = "users_list"
    def get_context_data(self, **kwargs):
        context=super().get_context_data()
        context['users_list'] = models.CustomUser.objects.filter(username__contains=self.kwargs.get('p'))
        return context

def usersearch(request):
    searchForm = CustomUserSearchForm(request.GET)
    # searchForm変数に正常なデータがあれば
    if searchForm.is_valid():
        username = searchForm.cleaned_data['username'] # keyword変数にフォームのキーワードを代入
        users = models.CustomUser.objects.filter(username=username) # キーワードを含むレコードをfilterメソッドで取り出し、articles変数に代入
    # それ以外の場合
    else:
        searchForm = CustomUserSearchForm() # searchForm変数をSearchFormオブジェクトで上書き
        users = models.CustomUser.objects.all() # すべてのレコードを取得
 
    context = {
    'users_list': users,
    'searchForm': searchForm, # テンプレートに渡すために追記
    }
    return render(request, 'user/list.html', context)

class UserDetailView(LoginRequiredMixin, mixins.BlockTestMixin, DetailView):
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
            models.Block.objects.get(blocked_id=self.kwargs.get('pk'),block_id=self.request.user.id)
            context['block_flag'] = True
        except:
            context['block_flag'] = False
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