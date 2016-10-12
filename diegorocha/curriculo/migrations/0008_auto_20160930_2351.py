# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-30 23:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('curriculo', '0007_auto_20160930_2321'),
    ]

    operations = [
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('degree', models.CharField(max_length=100, verbose_name='Degree')),
                ('status', models.CharField(choices=[('E', 'Em Curso'), ('C', 'Concluido')], default='E', max_length=1, verbose_name='Status')),
                ('start_year', models.IntegerField(verbose_name='Start')),
                ('end_year', models.IntegerField(blank=True, null=True, verbose_name='End')),
                ('description', models.TextField(verbose_name='Description')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='educations', to='curriculo.Profile')),
            ],
            options={
                'ordering': ['-start_year'],
            },
        ),
        migrations.AlterModelOptions(
            name='job',
            options={'ordering': ['-start_date']},
        ),
    ]
