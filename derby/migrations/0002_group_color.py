# Generated by Django 3.1.5 on 2021-02-07 19:14

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('derby', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='color',
            field=colorfield.fields.ColorField(default='##FF0000', max_length=18, unique=True),
        ),
    ]
