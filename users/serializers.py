from rest_framework import serializers

from django.contrib.auth import get_user_model

from users.validators import ValidatorSetPasswordUser
from users.handlers import HandleCreateUser
from library.serializers import OrderListViewSerializer


class UserProfileSerializer(serializers.ModelSerializer):
    """Сеарилизатор Профиля пользователя
    """
    orders = OrderListViewSerializer(many=True,
                                     source='order_set',
                                     )
    count_orders = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('id',
                  'username',
                  'first_name',
                  'last_name',
                  'email',
                  'phone',
                  'last_login',
                  'is_staff',
                  'groups',
                  'orders',
                  'count_orders',
                  )

    def get_count_orders(self, obj):
        return obj.order_set.count()


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

    def create(self, validated_data):
        instance = HandleCreateUser(self.Meta.model,
                                    validated_data,
                                    ).create()
        return instance


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
