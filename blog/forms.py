
from django import forms
from django.contrib import admin
from .models import Post, Ingredient
# from .models import Menu
from django.db.models.fields.related import ManyToManyRel
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from datetime import date
from django.db import models


class PostForm(forms.ModelForm):
    ingredients = forms.ModelMultipleChoiceField(
        Ingredient.objects.all(), widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    class Meta:
        model = Post
        fields = ('title', 'text', 'calories', 'price', 'image', 'ingredients')
        widgets = {
            'body': forms.Textarea(),
            'ingredients': forms.CheckboxSelectMultiple()
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



# class MenuForm(forms.ModelForm):
#     items = forms.ModelMultipleChoiceField(
#         Post.objects.all(), widget=forms.CheckboxSelectMultiple(),
#         required=False,
#     )
#
#     class Meta:
#         model = Menu
#         fields = ('items',)
#         widgets = {
#             'items': forms.CheckboxSelectMultiple()
#         }
#
#
#     def selected_ingredients_labels(self):
#         return [label for value, label in self.fields['items'].choices if value in self['items'].vallue()]
#
#     def save(self, *args, **kwargs):
#         instance = super(MenuForm, self).save(*args, **kwargs)
#         if instance.pk:
#             for item in instance.items.all():
#                 if item not in self.cleaned_data['items']:
#                     instance.ingredients.remove(item)
#             for item in self.cleaned_data['items']:
#                 if item not in instance.items.all():
#                     instance.items.add(item)
#         return instance
