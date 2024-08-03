import traceback
from typing import Dict, Union

from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

from users.validators import ValidatorSetPasswordUser


class UserProfileSerializer(serializers.ModelSerializer):
    """Сеарилизатор Профиля пользователя
    """

    class Meta:
        model = get_user_model()
        fields = ('id',
                  'username',
                  'tg_id',
                  'first_name',
                  'last_name',
                  'email',
                  'phone',
                  'last_login',
                  'is_staff',
                  'groups',
                  )


class UserProfileCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания Профиля
    """
    password_check = serializers.CharField(write_only=True, required=True,)

    class Meta:
        model = get_user_model()
        fields = ('id',
                  'username',
                  'first_name',
                  'last_name',
                  'email',
                  'phone',
                  'password',
                  'password_check',
                  )
        validators = [ValidatorSetPasswordUser(['password',
                                                'password_check',
                                                ])]

    def _create_user(self,
                     model: AbstractUser,
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
            instance = model._default_manager.create(**validated_data)
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
                    model.__name__,
                    model._default_manager.name,
                    model.__name__,
                    model._default_manager.name,
                    self.__class__.__name__,
                    tb
                )
            )
            raise TypeError(msg)

        return instance

    def create(self, validated_data: Dict) -> AbstractUser:
        """Точка входа для создания пользователя
        """
        ModelClass = self.Meta.model
        password = validated_data.pop('password_check')

        return self._create_user(ModelClass, password, validated_data)


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """Редактирование профиля пользователя
    """
    class Meta:
        model = get_user_model()
        fields = ('username',
                  'first_name',
                  'last_name',
                  'email',
                  'phone',
                  )
