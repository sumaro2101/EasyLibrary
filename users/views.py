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
        if not instance == request.user and not request.user.is_librarian:
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

    def get_permissions(self):
        anonymous = self.request.user.is_anonymous
        if anonymous or not self.request.user.is_librarian:
            return super().get_permissions()
        else:
            self.permission_classes = [permissions.IsAuthenticated &
                                       IsSuperUser]
        return super().get_permissions()


class UserUpdateProfileAPI(generics.UpdateAPIView):
    """Редактирование пользователя
    """
    queryset = get_user_model().objects.get_queryset()
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated &
                          (IsCurrentUser | IsSuperUser)]

    def get_permissions(self):
        if not self.request.user.is_librarian:
            return super().get_permissions()
        else:
            self.permission_classes = [permissions.IsAuthenticated &
                                       IsSuperUser]
        return super().get_permissions()


class UserDeleteProfuleAPI(generics.DestroyAPIView):
    """Изменение активности пользователя
    """
    queryset = get_user_model().objects.get_queryset()
    permission_classes = [permissions.IsAuthenticated &
                          (IsCurrentUser | IsSuperUser)]

    def perform_destroy(self, instance: AbstractUser) -> None:
        instance.is_active = False
        instance.save(update_fields=('is_active',))

    def get_permissions(self):
        librarian = self.request.user.is_librarian
        if not librarian:
            return super().get_permissions()
        else:
            self.permission_classes = [permissions.IsAuthenticated &
                                       IsSuperUser]
        return super().get_permissions()


class LibrarianCreateProfileAPI(generics.CreateAPIView):
    """Создание библиотекаря,
    может создать только администратор
    """
    queryset = get_user_model().objects.get_queryset()
    serializer_class = UserProfileCreateSerializer
    permission_classes = [permissions.IsAuthenticated & IsSuperUser]

    def perform_create(self, serializer):
        serializer.save(is_staff=True, is_librarian=True)
