from django import forms
from django.contrib import admin
from .models import Post, Ingredient
from django.db.models.fields.related import ManyToManyRel
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from datetime import date
from django.db import models


class PostForm(forms.ModelForm):
    ingredients = forms.ModelMultipleChoiceField(
        Ingredient.objects.all(),
        required=False,
    )

    class Meta:
        model = Post
        fields = ('title', 'text', 'calories', 'price', 'image', 'ingredients')
        widgets = {
            'body': forms.Textarea(),
            'ingredients': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.initial['ingredients'] = self.instance.ingredients.values_list('pk', flat=True)
            rel = ManyToManyRel(Ingredient)
            self.fields['ingredients'].widget = RelatedFieldWidgetWrapper(self.fields['ingredients'].widget, rel,
                                                                          admin.site)

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


class IngredientsForm(forms.ModelForms):
    class Meta:
        model = Ingredient
        fields = ('name', 'weight', 'prise')
