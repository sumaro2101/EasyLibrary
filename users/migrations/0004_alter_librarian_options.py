# Generated by Django 5.0.7 on 2024-08-03 19:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_librarian'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='librarian',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
    ]
