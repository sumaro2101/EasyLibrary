from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.base_user import AbstractBaseUser

from rest_framework_simplejwt.authentication import JWTAuthentication

from users.models import Librarian


class LibrarianAuthBackend(ModelBackend):
    """Обработка аунтификации библиотекаря
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = Librarian
        try:
            user = user_model.objects.get(email=username)
            if user.check_password(password) and user.is_active:
                return user
            return None
        except (user_model.DoesNotExist, user_model.MultipleObjectsReturned):
            return None

    def get_user(self, user_id: int) -> AbstractBaseUser | None:
        user_model = Librarian
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None


class LibrarianJWTAuthBackend(JWTAuthentication):
    """Аунтификация по JWT токену
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.user_model = Librarian
