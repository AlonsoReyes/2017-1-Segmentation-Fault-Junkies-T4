# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-29 20:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20170529_1417'),
    ]

    operations = [
        migrations.AddField(
            model_name='transacciones',
            name='nombreComida',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
