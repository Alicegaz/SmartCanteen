from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from blog.widgets import *
from blog.fields import *
from django.db.models import IntegerField, Model
from django.core.validators import MaxValueValidator, MinValueValidator

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
TYPE_CHOICES_SHARES = (
    ('скидка', 'скидка'),
    ('распродажа', 'распродажа'),
    ('подарок за покупку', 'подарок за покупку'),
)


class Ingredient(models.Model):
    name = models.CharField(max_length=300)
    weight = models.IntegerField(null=True)
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
    title = models.CharField(max_length=70, verbose_name='Название блюда',default='')
    text = models.TextField(verbose_name='Описание', default='')
    calories = models.BigIntegerField(null=True, blank=True, verbose_name='калории', default=0)
    price = models.BigIntegerField(null=True, default=0, error_messages={'required': 'Determine the price'},
                                   verbose_name='цена')
    created_date = models.DateTimeField(default=timezone.now)
    image = models.FileField(null=True, upload_to='images/dishes', verbose_name='изображение блюда')
    type = models.CharField(max_length=50, verbose_name='Тип ', default='First', choices=TYPE_CHOICES)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.choice_text

    def get_json_object(self):
        dic = self.__dict__
        dic['created_date'] = self.created_date.isocalendar()
        if self.image:
            dic['image'] = self.image.url
        else:
            dic['image'] = ''
        dic.pop('_state')
        return dic

    def get_ingredients(self):
        ing_relation = IngDishRelation.objects.filter(dish=self)
        result = []
        for instance in ing_relation:
            result.append(instance.ingredient)
        return result

    def get_amount(self, ingredient):
        ing_r = IngDishRelation.objects.get(dish=self, ingredient=ingredient)
        return ing_r.amount


class IngDishRelation(models.Model):
    dish = models.ForeignKey(Post, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField(null=False)

    def subtract_from_ingredient(self):
        self.ingredient.weight -= self.amount
        self.ingredient.save()


class Menu(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=60, default='')
    date = models.DateTimeField(default=timezone.now)
    items = models.ManyToManyField(Post)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.choice_text

    def enable_to_subtract_from_ingredient(self):
        result = True
        for item in self.items.all():
            ing_dish_relations = IngDishRelation.objects.filter(dish=item)
            for relation in ing_dish_relations:
                one_more = (relation.ingredient.weight >= relation.amount)
                result = result or one_more
        return True

    def subtract_from_ingredient(self):
        for item in self.items.all():
            ing_dish_relations = IngDishRelation.objects.filter(dish=item)
            for relation in ing_dish_relations:
                relation.subtract_from_ingredient()

    def get_json_object(self):
        result = []
        for item in self.items.all():
            result.append(item.get_json_object())
        return result


class History(models.Model):
    menu = models.ForeignKey(Menu)


class Schedule(models.Model):
    monfr1 = models.DateTimeField(auto_now=True, null=True)
    stsn1 = models.DateTimeField(auto_now=True, null=True)
    dinner1 = models.DateTimeField(auto_now=True, null=True)
    breakfast1 = models.DateTimeField(auto_now=True, null=True)
    supper1 = models.DateTimeField(auto_now=True, null=True)
    monfr2 = models.DateTimeField(auto_now=True, null=True)
    stsn2 = models.DateTimeField(auto_now=True, null=True)
    dinner2 = models.DateTimeField(auto_now=True, null=True)
    breakfast2 = models.DateTimeField(auto_now=True, null=True)
    supper2 = models.DateTimeField(auto_now=True, null=True)
    image = models.FileField(null=True, upload_to='images/dishes', verbose_name='фон')
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.stsn1


class Shares(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200, verbose_name='Название блюда')
    type = models.CharField(max_length=50, verbose_name='Тип ', choices=TYPE_CHOICES_SHARES)
    text = models.TextField(verbose_name='Описание')
    start_date = models.DateTimeField(default=timezone.now, blank=True)
    end_date = models.DateTimeField(default=timezone.now, blank=True)
    old_price = models.BigIntegerField(null=True, blank=True, verbose_name='старая цена')
    new_price = models.BigIntegerField(null=True, blank=True, verbose_name='новая цена')
    discount = IntegerField(null=True, blank=True, default=1,
                            validators=[
                                MaxValueValidator(100),
                                MinValueValidator(1)
                            ], verbose_name='скидка')
    created_date = models.DateTimeField(default=timezone.now)
    image = models.FileField(null=True, upload_to='images/dishes', verbose_name='изображение блюда')
    carousel = models.BooleanField(default=True)

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


class Offers(models.Model):
    date = models.DateField(default=timezone.now)
    items = models.ManyToManyField(Post)
    menu = models.ForeignKey(Menu)
    status = models.BooleanField(default=False)