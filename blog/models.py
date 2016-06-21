from itertools import chain

from django.db import models
from django.forms import RadioSelect, CheckboxSelectMultiple, CheckboxInput
from django.utils import timezone
from django import forms
from django.core.exceptions import ValidationError
from requests import auth

TYPE_CHOICES = (
    ('First', 'Первое'),
    ('Second', 'Гарнир'),
    ('Third', 'Второе'),
    ('Self', 'Самостоятельное'),
    ('Salad', 'Салат'),
    ('Baverage', 'Напиток'),
)
TYPE_MENU_CHOICES = (
    ('dinner', 'обед'),
    ('breakfast', 'завтрак'),
    ('supper', 'ужин'),
)


class Ingredient(models.Model):
    name = models.CharField(max_length=300)
    #author = models.ForeignKey('auth.User')
    weight = models.IntegerField(null=True)
    price = models.IntegerField(null=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

        # def __init__(self, *args, **kwargs):
        # super(models.Model, self).__init__(*args, **kwargs)
        # adding css classes to widgets without define the fields:
        # for field in self.fields:
        #    self.fields[field].widget.attrs['class'] = 'form-control'

    class Meta:
        ordering = ('name',)


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200, verbose_name='Название блюда')
    text = models.TextField(verbose_name='Описание')
    calories = models.BigIntegerField(null=True, blank=True, verbose_name='калории')
    price = models.BigIntegerField(null=True, error_messages={'required': 'Determine the price'}, verbose_name='цена')
    created_date = models.DateTimeField(default=timezone.now)
    image = models.FileField(null=True, upload_to='images/dishes', verbose_name='изображение блюда')
    published_date = models.DateTimeField(blank=True, null=True)
    ingredients = models.ManyToManyField(Ingredient, verbose_name='список продуктов')
    type = models.CharField(max_length=50, verbose_name='Тип ', choices=TYPE_CHOICES)

    # pic = models.ImageField(blank=True, )

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.choice_text

    def get_json_object(self):
        dic = self.__dict__
        dic['created_date'] = self.created_date.isocalendar()
        dic['published_date']=self.created_date.isocalendar()
        dic.pop('_state')
        return dic

class Menu(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=1, choices=TYPE_MENU_CHOICES)
    date = models.DateTimeField(blank=True, null=True)
    items = models.ManyToManyField(Post)

    # pic = models.ImageField(blank=True, )

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.choice_text


def clean_price(self):
    if self.clean_data.get('price') < 0:
        raise ValidationError("Значение цены должно быть положительным!", code="invalid")
