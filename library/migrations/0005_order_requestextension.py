# Generated by Django 5.0.7 on 2024-08-08 13:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_alter_book_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count_extensions', models.SmallIntegerField(default=0, help_text='Количество продлений которые уже были сделаны', verbose_name='продления')),
                ('time_order', models.DateField(auto_now_add=True, help_text='Время когда книга была выдана', verbose_name='время выдачи')),
                ('time_return', models.DateField(help_text='Время когда нужно вернуть книгу', verbose_name='время возврата')),
                ('status', models.CharField(choices=[('active', 'активно'), ('end', 'закончено')], default='active')),
                ('book', models.ForeignKey(help_text='Книга которую выдали', on_delete=django.db.models.deletion.CASCADE, to='library.book', verbose_name='книга')),
                ('tenant', models.ForeignKey(help_text='На кого была выдана книга', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'выдача',
                'verbose_name_plural': 'выдачи',
                'ordering': ['time_order'],
            },
        ),
        migrations.CreateModel(
            name='RequestExtension',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_request', models.DateTimeField(auto_now_add=True, help_text='Время запроса', verbose_name='время запроса')),
                ('time_response', models.DateTimeField(auto_now=True, help_text='Время ответа', verbose_name='время ответа')),
                ('solution', models.CharField(choices=[('accept', 'принят'), ('cancel', 'отменен')], help_text='Принятое решение библиотекарем', verbose_name='решение')),
                ('order', models.ForeignKey(help_text='Объект выдачи книги', on_delete=django.db.models.deletion.CASCADE, to='library.order', verbose_name='выдача')),
                ('receiving', models.ForeignKey(default=None, help_text='Библиотекарь который обработал запрос', on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL, verbose_name='принимающий')),
            ],
            options={
                'verbose_name': 'запрос',
                'verbose_name_plural': 'запросы',
                'ordering': ['time_request'],
            },
        ),
    ]
