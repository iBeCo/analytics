# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-17 12:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[(b'admin', b'Admin'), (b'customer', b'Customer'), (b'retailer', b'Retailer'), (b'associate', b'Associate')], default=b'customer', max_length=25, verbose_name='Role'),
        ),
    ]
