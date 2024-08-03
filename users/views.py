from rest_framework import generics, permissions
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

from users.serializers import (UserProfileSerializer,
                               UserProfileCreateSerializer,
                               UserProfileUpdateSerializer,
                               )
from users.permissions import IsCurrentUser, IsSuperUser


class UserProfileViewAPI(generics.RetrieveAPIView):
    """Профиль пользователя
    """
    queryset = get_user_model().objects.filter(is_active=True)
    serializer_class = UserProfileSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if not instance == request.user:
            list_of_allow_fields = ('username',
                                    'first_name',
                                    'email',
                                    'is_staff',
                                    'groups',
                                    )
            data = {key: value for key, value in serializer.data.items()
                    if key in list_of_allow_fields}
            return Response(data)

        return Response(serializer.data)


class UserCreateProfileAPI(generics.CreateAPIView):
    """Создание нового пользователя
    """
    queryset = get_user_model().objects.get_queryset()
    serializer_class = UserProfileCreateSerializer
    permission_classes = [permissions.AllowAny]


class UserUpdateProfileAPI(generics.UpdateAPIView):
    """Редактирование пользователя
    """
    queryset = get_user_model().objects.get_queryset()
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [IsCurrentUser | IsSuperUser]


class UserDeleteProfuleAPI(generics.DestroyAPIView):
    """Изменение активности пользователя
    """
    queryset = get_user_model().objects.get_queryset()
    permission_classes = [permissions.IsAuthenticated &
                          (IsCurrentUser | IsSuperUser)]

    def perform_destroy(self, instance: AbstractUser) -> None:
        instance.is_active = False
        instance.save(update_fields=('is_active',))
