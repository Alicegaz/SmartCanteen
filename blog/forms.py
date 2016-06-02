from django import forms
from django.contrib import admin
from .models import Post, Ingredient
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


class IngredientsForm(forms.ModelForms):
    class Meta:
        model = Ingredient
        fields = ('name', 'weight', 'prise')