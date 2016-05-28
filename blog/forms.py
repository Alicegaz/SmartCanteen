from django import forms
from .models import Post
from datetime import date
from django.db import models

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'calories', 'price', 'image')
