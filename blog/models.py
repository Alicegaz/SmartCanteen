from django.db import models
from django.utils import timezone
from django import forms
# from PIL import Image
from django.core.exceptions import ValidationError


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    kkal = models.BigIntegerField(null=True, blank=True)
    price = models.BigIntegerField(null=True, error_messages={'required': 'Укажите цену'})
    created_date = models.DateTimeField(default=timezone.now)
    image = models.FileField(null=True, upload_to='images/dishes')
    published_date = models.DateTimeField(blank=True, null=True)
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

 #Create your models here.
