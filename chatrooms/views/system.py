from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail, EmailMultiAlternatives
from .. import models, forms
from chatrooms.forms import LoginForm, CustomUserCreationForm
import datetime

from django.template.loader import get_template

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
            'form': forms.ConfigForm
        }
        return self.render_to_response(ctx)
    
    def post(self, request, **kwargs):
        config = models.Config.objects.get(user=self.request.user)

        print(request.POST['message'])
        print(request.POST['notice'])
        config.message = request.POST['message']
        config.notice = request.POST['notice']
        config.room_post_log = request.POST['room_post_log']
        config.friend = request.POST['friend']
        config.save()
        return redirect('cf')




class DevelopmentView(TemplateView):
    template_name = 'system/development.html'
    def get(self, request, **kwargs):
        self.meeru_okuru()

        return redirect('rl')

    def meeru_okuru(self):
        subject = 'メール送信テスト'
        message = 'やっほー'
        html_content = f"""
        <p>やほほー</p>
        """
        sent = 'aqurine117@gmail.com'
        receive = 'wakanohibiki0131@gmail.com'
        msg = EmailMultiAlternatives(
        subject, 
        message, 
        sent, 
        [receive])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return 0

    """
    def get(self, request, **kwargs):
        for user in models.CustomUser.objects.all():
            print(user)
            models.Config.objects.create(
                user = user,
            )
        return redirect('rl')"""

class NavSearch(TemplateView):
    template_name = 'user/list.html'
    def get(self,request,**kwargs):
        inputed = request.GET['userid']
        context={}
        context['users_list']=models.CustomUser.objects.filter(username__contains=inputed)
        #return redirect('rl')
        return self.render_to_response(context)