# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-24 12:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20171023_1344'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='signature',
            field=models.CharField(blank=True, max_length=25, null=True, verbose_name='Signature'),
        ),
    ]
