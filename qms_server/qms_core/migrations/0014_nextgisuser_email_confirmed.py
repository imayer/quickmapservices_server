# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-11-14 00:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qms_core', '0013_auto_20161026_1238'),
    ]

    operations = [
        migrations.AddField(
            model_name='nextgisuser',
            name='email_confirmed',
            field=models.BooleanField(default=False, verbose_name='mail confirmed'),
        ),
    ]
