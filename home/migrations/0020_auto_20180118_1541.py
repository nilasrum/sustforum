# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-01-18 15:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0019_auto_20180118_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='color',
            field=models.CharField(default=b'#46b8da', max_length=255),
        ),
    ]
