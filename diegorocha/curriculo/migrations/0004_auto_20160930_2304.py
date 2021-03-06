# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-30 23:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curriculo', '0003_auto_20160930_2302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='education_title',
            field=models.CharField(max_length=100, null=True, verbose_name='Education Title'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='experience_title',
            field=models.CharField(max_length=100, null=True, verbose_name='Experience Title'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_title',
            field=models.CharField(max_length=100, verbose_name='Profile Title'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='subtitle',
            field=models.CharField(max_length=100, verbose_name='Subtitle'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='title',
            field=models.CharField(max_length=100, verbose_name='Title'),
        ),
    ]
