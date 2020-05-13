# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-05-09 05:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reads_app', '0004_auto_20200509_0421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='reviewer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_reviews', to='reads_app.User'),
        ),
    ]