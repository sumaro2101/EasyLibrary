# Generated by Django 5.0.7 on 2024-08-10 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_book_quantity_order_requestextension'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('active', 'активно'), ('end', 'закончено')], default='active', max_length=30),
        ),
        migrations.AlterField(
            model_name='requestextension',
            name='solution',
            field=models.CharField(choices=[('accept', 'принят'), ('cancel', 'отменен'), ('wait', 'ожидание')], default='wait', help_text='Принятое решение библиотекарем', max_length=30, verbose_name='решение'),
        ),
    ]