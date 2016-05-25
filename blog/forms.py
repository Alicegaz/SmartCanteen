from django import forms
from .models import Post
from datetime import date


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'pic')
