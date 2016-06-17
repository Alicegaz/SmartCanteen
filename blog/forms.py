from itertools import chain

from django import forms
from django.forms import ChoiceField, CheckboxSelectMultiple, CheckboxInput
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from .models import Menu
from .models import Post, Ingredient, TYPE_CHOICES, TYPE_MENU_CHOICES


class PostForm(forms.ModelForm):
    ingredients = forms.ModelMultipleChoiceField(
        Ingredient.objects.all(), widget=forms.CheckboxSelectMultiple(),
        required=False,
    )
    type = forms.ChoiceField(widget=forms.Select(), choices=TYPE_CHOICES)

    # type = forms.ChiceField(widget=forms.RadioSelect, choices = TYPE_CHOICES)


    class Meta:
        model = Post
        fields = ('title', 'text', 'calories', 'price', 'image', 'ingredients', 'type')
        widgets = {
            'body': forms.Textarea(),
            'ingredients': forms.CheckboxSelectMultiple(),
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


class IngredientsForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ('name', 'weight')


class MenuForm(forms.ModelForm):
    items = forms.ModelMultipleChoiceField(
        Post.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={'class':'chosen'}),
        required=False,
    )
    title = forms.ChoiceField(widget=forms.Select(), choices=TYPE_MENU_CHOICES)

    class Meta:
        model = Menu
        fields = ('items', 'title')
        widgets = {
            'items': forms.CheckboxSelectMultiple(attrs={'class':'chosen'}),
            'title': forms.ChoiceField(widget=forms.Select(), choices=TYPE_MENU_CHOICES),
        }

    def selected_ingredients_labels(self):
        return [label for value, label in self.fields['items'].choices if value in self['items'].vallue()]

    def save(self, *args, **kwargs):
        instance = super(MenuForm, self).save(*args, **kwargs)
        if instance.pk:
            for item in instance.items.all():
                if item not in self.cleaned_data['items']:
                    instance.ingredients.remove(item)
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

