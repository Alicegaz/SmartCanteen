# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-30 08:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_ingredient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='included_to',
            field=models.ManyToManyField(blank=True, related_name='ingredients', to='blog.Post'),
        ),
    ]