from django import forms
from .models import Post, CustomUser
from django.contrib.auth.forms import UserCreationForm

class Response(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('text',)
        label = ('本文',)

class LoginForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2']