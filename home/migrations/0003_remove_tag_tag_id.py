# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-11-26 20:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20171126_2001'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='tag_id',
        ),
    ]
