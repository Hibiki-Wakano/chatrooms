from django import forms
from .models import Post

class Response(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('text',)
        label = ('本文',)