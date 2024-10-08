# Generated by Django 5.0.7 on 2024-08-14 09:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0006_alter_book_best_seller'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='tenant',
            field=models.ForeignKey(help_text='На кого была выдана книга', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
        migrations.AlterField(
            model_name='requestextension',
            name='applicant',
            field=models.ForeignKey(blank=True, default=None, help_text='Заявщик который хочет продлить', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='extensions', to=settings.AUTH_USER_MODEL, verbose_name='заявщик'),
        ),
    ]
