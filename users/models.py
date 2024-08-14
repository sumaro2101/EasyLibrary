from django.contrib.auth.models import AbstractUser
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class User(AbstractUser):
    """Модель пользователя
    """
    email = models.EmailField(unique=True,
                              verbose_name='эмеил',
                              help_text='Эмеил пользователя',
                              )

    phone = PhoneNumberField(help_text='Номер телефона,\
        важно указать для связи с клиентом.\
            Пример: +7 (900) 910 1000',
                             unique=True,
                             )

    is_librarian = models.BooleanField(default=False,
                                       editable=False,
                                       verbose_name='библиотекарь',
                                       help_text='Обозначение библитекаря',
                                       )
