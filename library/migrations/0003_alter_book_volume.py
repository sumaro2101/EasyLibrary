# Generated by Django 5.0.7 on 2024-08-07 18:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_alter_book_best_seller_alter_book_is_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='volume',
            field=models.ForeignKey(blank=True, help_text='Том книги', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='books', to='library.volume', verbose_name='том'),
        ),
    ]