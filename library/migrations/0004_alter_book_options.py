# Generated by Django 5.0.7 on 2024-08-08 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_alter_book_volume'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['name'], 'verbose_name': 'Книга', 'verbose_name_plural': 'Книги'},
        ),
    ]
