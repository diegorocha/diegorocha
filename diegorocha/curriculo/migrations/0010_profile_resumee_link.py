# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-10-12 03:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curriculo', '0009_socialmedia'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='resumee_link',
            field=models.URLField(default='', verbose_name='Link Resumee'),
        ),
    ]
