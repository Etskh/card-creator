# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-17 08:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0005_auto_20170214_1308'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='field',
            name='style',
        ),
    ]