# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-06-04 04:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curriculo', '0010_profile_resumee_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='education',
            name='status',
            field=models.CharField(choices=[('E', 'Em Curso'), ('T', 'Trancado'), ('C', 'Concluido')], default='E', max_length=1, verbose_name='Status'),
        ),
    ]
