# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2016-11-10 19:43
from __future__ import unicode_literals

from django.db import migrations, models
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_photos'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='photo',
            options={'verbose_name': 'Foto', 'verbose_name_plural': 'Fotos'},
        ),
        migrations.AlterModelOptions(
            name='photos',
            options={'verbose_name': 'Foto', 'verbose_name_plural': 'Fotos'},
        ),
        migrations.AlterField(
            model_name='photo',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creacion'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='date_modified',
            field=models.DateTimeField(auto_now=True, verbose_name='Fecha de Modificacion'),
        ),
        migrations.AlterField(
            model_name='photos',
            name='image',
            field=filebrowser.fields.FileBrowseField(max_length=200, verbose_name='Foto'),
        ),
    ]
