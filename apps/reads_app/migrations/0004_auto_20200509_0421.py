# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-05-09 04:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reads_app', '0003_auto_20200509_0411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='book_reviewed',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='reads_app.Book'),
        ),
        migrations.AlterField(
            model_name='review',
            name='reviewer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='reads_app.User'),
        ),
    ]
