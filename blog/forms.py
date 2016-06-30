from django import forms
from datetime import timezone
from django.forms import ChoiceField
from .models import Post, Ingredient, TYPE_CHOICES, TYPE_MENU_CHOICES, Menu, IngDishRelation
from blog.fields import *
from common.request import get_image_from_request
from common.blog_post_list import get_menu_of_current_time

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
        request = kwargs['request']
        instance = super(PostForm, self).save(commit=False)
        instance.author = request.user
        instance.save()
        quantity_list = kwargs['quantity_list']
        for (item, quantity) in zip(self.cleaned_data.get('ingredients'), quantity_list):
            ing_r = IngDishRelation.objects.create(dish=instance, ingredient=item, amount=quantity)
            ing_r.save()

        return instance

    def save_object(self, **kwargs):
        instance = super(PostForm, self).save(commit=False)
        request = kwargs['request']
        instance.author = request.user
        image = get_image_from_request(request)
        if image:
            instance.image = image
        instance.save()
        for ing_r in IngDishRelation.objects.filter(dish=instance):
            ing_r.delete()
        quantity_list = request.POST.getlist('quantity')
        for (item, quantity) in zip(self.cleaned_data.get('ingredients'), quantity_list):
            ing_r = IngDishRelation.objects.create(dish=instance, ingredient=item, amount=quantity)
            ing_r.save()
        return instance

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        # adding css classes to widgets without define the fields:
        for field in self.fields:
            #self.fields[field].widget.attrs['class'] = 'form-control'
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
    title = forms.ChoiceField(widget=forms.Select(), choices=TYPE_MENU_CHOICES)

    class Meta:
        model = Menu
        fields = ('items', 'title')

        widgets = {
            'items': forms.CheckboxSelectMultiple(attrs={'class': 'chosen'}),
            'title': forms.ChoiceField(widget=forms.Select(), choices=TYPE_MENU_CHOICES),
        }

    def selected_ingredients_labels(self):
        return [label for value, label in self.fields['items'].choices if value in self['items'].vallue()]

    def save(self, *args, **kwargs):
        menus = get_menu_of_current_time(self.cleaned_data['title'])
        for menu in menus:
            menu.delete()
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


