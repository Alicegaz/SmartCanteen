from datetime import timezone
from itertools import chain

from django import forms
from django.forms import ChoiceField, CheckboxSelectMultiple, CheckboxInput, SelectDateWidget
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from .models import Menu
from .models import Post, Ingredient, TYPE_CHOICES, TYPE_MENU_CHOICES
from django.utils import timezone
from django.forms.extras.widgets import SelectDateWidget
import re
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import Widget, Select, MultiWidget
from django.utils.safestring import mark_safe
from blog.widgets import *
from blog.fields import *


class ElectionTimesForm(forms.Form):
  # times
  voting_starts_at = SplitDateTimeField(help_text = 'UTC date and time when voting begins',
                                   widget=SplitSelectDateTimeWidget)
  voting_ends_at = SplitDateTimeField(help_text = 'UTC date and time when voting ends',
                                   widget=SplitSelectDateTimeWidget)



class PostForm(forms.ModelForm):
    ingredients = forms.ModelMultipleChoiceField(
        Ingredient.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={'class': 'chosen'}),
        required=False,
    )
    type = forms.ChoiceField(widget=forms.Select(), choices=TYPE_CHOICES)

    # type = forms.ChiceField(widget=forms.RadioSelect, choices = TYPE_CHOICES)


    class Meta:
        model = Post
        fields = ('title', 'text', 'calories', 'price', 'image', 'ingredients', 'type')
        widgets = {
            'body': forms.Textarea(),
            'ingredients': forms.CheckboxSelectMultiple(attrs={'class': 'chosen'}),
            'type': ChoiceField(choices=TYPE_CHOICES, widget=forms.Select()),
        }

    def selected_ingredients_labels(self):
        return [label for value, label in self.fields['ingredients'].choices if value in self['ingredients'].vallue()]

    def save(self, *args, **kwargs):
        instance = super(PostForm, self).save(*args, **kwargs)
        if instance.pk:
            for ingredient in instance.ingredients.all():
                if ingredient not in self.cleaned_data['ingredients']:
                    instance.ingredients.remove(ingredient)
            for ingredient in self.cleaned_data['ingredients']:
                if ingredient not in instance.ingredients.all():
                    instance.ingredients.add(ingredient)
        return instance

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        # adding css classes to widgets without define the fields:
        for field in self.fields:
            self.fields['ingredients'].widget.attrs['class'] = 'chosen'


class IngredientsForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ('name', 'weight')


class MenuForm(forms.ModelForm):
    items = forms.ModelMultipleChoiceField(
        Post.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={'class': 'chosen'}),
        required=False,
    )
    # title = forms.ChoiceField(widget=forms.Select(), choices=TYPE_MENU_CHOICES)
    #title = forms.CharField()
    date = forms.DateField(widget=SelectDateWidget(), initial=timezone.now)
    #times = forms.TimeField(widget=SelectTimeWidget(twelve_hr=True), label=u'Time')

    class Meta:
        model = Menu
        fields = ('items', 'date', 'times')

        widgets = {
            'items': forms.CheckboxSelectMultiple(attrs={'class': 'chosen'}),
            'date': forms.DateField(widget=SelectDateWidget(), initial=timezone.now),
            #'times': forms.TimeField(widget=SelectTimeWidget(twelve_hr=True), label=u'Time')
            # default=datetime.now
            # 'title': forms.ChoiceField(widget=forms.Select(), choices=TYPE_MENU_CHOICES),
        }

    def selected_ingredients_labels(self):
        return [label for value, label in self.fields['items'].choices if value in self['items'].vallue()]

    def save(self, *args, **kwargs):
        instance = super(MenuForm, self).save(*args, **kwargs)
        if instance.pk:
            for item in instance.items.all():
                if item not in self.cleaned_data['items']:
                    instance.items.remove(item)
            for item in self.cleaned_data['items']:
                if item not in instance.items.all():
                    instance.items.add(item)
        return instance

    def __init__(self, *args, **kwargs):
        super(MenuForm, self).__init__(*args, **kwargs)
        # adding css classes to widgets without define the fields:
        for field in self.fields:
            self.fields['items'].widget.attrs['class'] = 'chosen'
            # class PostIngredient(models.Model):
            # post = models.ForeighKey(Post)
            # ingredient = models.ForeignKey(Ingredient)
