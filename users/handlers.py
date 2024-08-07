import traceback
from typing import Dict, Union

from django.contrib.auth.models import AbstractUser


class HandleCreateUser:
    """Обработчик создания пользователя
    """

    def __init__(self,
                 model: AbstractUser,
                 validated_data: Dict,
                 ) -> None:
        if not issubclass(model, AbstractUser):
            raise TypeError(f'{model}, должен быть моделью пользователя')
        if not isinstance(validated_data, Dict):
            raise TypeError(f'{validated_data}, должен быть словарем')
        self.model = model
        self.validated_data = validated_data

    def _create_user(self,
                     password: str,
                     validated_data: Dict,
                     ) -> Union[AbstractUser, None]:
        """Создание пользователя

        Args:
            model (AbstractUser): Модель User
            password (str): Возможный пароль
            validated_data (Dict): Валидная информация

        Returns:
            Union[AbstractUser, None]: Возращает созданного пользователя
            в случае успеха
        """
        try:
            instance = self.model._default_manager.create(**validated_data)
            instance.set_password(password)
            instance.save(update_fields=['password'])
        except TypeError:
            tb = traceback.format_exc()
            msg = (
                'Got a `TypeError` when calling `%s.%s.create()`. '
                'This may be because you have a writable field on the '
                'serializer class that is not a valid argument to '
                '`%s.%s.create()`. You may need to make the field '
                'read-only, or override the %s.create() method to handle '
                'this correctly.\nOriginal exception was:\n %s' %
                (
                    self.model.__name__,
                    self.model._default_manager.name,
                    self.model.__name__,
                    self.model._default_manager.name,
                    self.__class__.__name__,
                    tb
                )
            )
            raise TypeError(msg)

        return instance

    def create(self) -> AbstractUser:
        """Точка входа для создания пользователя
        """
        password = self.validated_data.pop('password_check')

        return self._create_user(password, self.validated_data)
