# Generated by Django 5.0.7 on 2024-08-07 13:45

import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_librarian',
            field=models.BooleanField(default=False, editable=False, help_text='Обозначение библитекаря', verbose_name='библиотекарь'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(help_text='Номер телефона,        важно указать для связи с клиентом.            Пример: +7 (900) 910 1000', max_length=128, region=None, unique=True),
        ),
    ]
