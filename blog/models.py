from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from blog.widgets import *
from blog.fields import *


TYPE_CHOICES = (
    ('First', 'Первое'),
    ('Second', 'Гарнир'),
    ('Third', 'Второе'),
    ('Self', 'Самостоятельное'),
    ('Salad', 'Салат'),
    ('Baverage', 'Напиток'),
)
TYPE_MENU_CHOICES = (
    ('обед', 'обед'),
    ('завтрак', 'завтрак'),
    ('ужин', 'ужин'),
)


class Ingredient(models.Model):
    name = models.CharField(max_length=300)
    weight = models.IntegerField(null=True)
    price = models.IntegerField(null=True)
    date = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def get_json_object(self):
        dic = self.__dict__
        dic['date'] = self.date.isocalendar()
        dic.pop('_state')
        return dic

    class Meta:
        ordering = ('date',)


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200, verbose_name='Название блюда')
    text = models.TextField(verbose_name='Описание')
    calories = models.BigIntegerField(null=True, blank=True, verbose_name='калории')
    price = models.BigIntegerField(null=True, error_messages={'required': 'Determine the price'}, verbose_name='цена')
    created_date = models.DateTimeField(default=timezone.now)
    image = models.FileField(null=True, upload_to='images/dishes', verbose_name='изображение блюда')
    type = models.CharField(max_length=50, verbose_name='Тип ', choices=TYPE_CHOICES)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.choice_text

    def get_json_object(self):
        dic = self.__dict__
        dic['created_date'] = self.created_date.isocalendar()
        dic['image'] = self.image.url
        dic.pop('_state')
        return dic

    def get_ingredients(self):
        ing_relation = IngDishRelation.objects.filter(dish=self)
        result = []
        for instance in ing_relation:
            result.append(instance.ingredient)
        return result


class IngDishRelation(models.Model):
    dish = models.ForeignKey(Post, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField(null=False)

    def subtract_from_ingredient(self):
        self.ingredient.weight -= self.amount
        History.add_history_instance(relation=self)


class MenuObject(models.Model):
    ing_dish_relations = models.ManyToManyField(IngDishRelation)


class Menu(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=60, choices=TYPE_MENU_CHOICES)
    date = models.DateTimeField(default=timezone.now)
    items = models.ManyToManyField(Post)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.choice_text


class History(models.Model):
    dish = models.ForeignKey(Post)
    ingredient = models.ForeignKey(Ingredient)
    amount = models.IntegerField()
    date = models.DateField(default=timezone.now)

    def add_history_instance(self, relation):
        self.dish = relation.dish
        self.ingredient = relation.ingredient
        self.amount = relation.amount
        self.save()
