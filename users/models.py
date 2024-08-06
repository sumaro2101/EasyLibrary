from django.contrib.auth.models import AbstractUser
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class User(AbstractUser):
    """Модель пользователя
    """
    phone = PhoneNumberField(help_text='Номер телефона,\
        важно указать для связи с клиентом.\
            Пример: +7 (900) 910 1000',
                             unique=True,
                             )


class Librarian(User):
    """Модель библиотекаря
    """
