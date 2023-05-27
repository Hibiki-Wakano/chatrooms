from django import forms
from .models import Post, CustomUser, Message, Config
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label  

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username','user_name','icon',)

class CustomUserUpdateForm(forms.ModelForm): #ModelFromを継承してFormクラスを生成する
    class Meta:
        model = CustomUser
        fields = ('user_name','icon','memo')

class CustomUserSearchForm(forms.ModelForm):
    username = forms.CharField(
        initial='',
        label='ユーザーID',
        required = False, # 必須ではない
    )

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'rows':2, 'cols':60}),
        }

class MessageCreateForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('text','image',)
        widgets = {
            'text': forms.Textarea(attrs={'rows':1, 'cols':45}),
        }

class Configorm(forms.ModelForm):

    class Meta:
        model = Config
        fields = ("darkmode", "message_only_connected")