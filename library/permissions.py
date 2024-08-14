from rest_framework.permissions import BasePermission
from rest_framework import status


class IsLibrarian(BasePermission):
    """Права доступа библиотекаря
    """
    message = {
        'forbidden': 'Это действие может совершать только библиотекарь',
        }
    code = status.HTTP_403_FORBIDDEN

    def has_permission(self, request, view):
        return request.user.is_librarian


class IsSuperUser(BasePermission):
    """Проверка прав доступа администратора
    """
    def has_permission(self, request, view):
        return request.user.is_superuser


class IsCurrentUser(BasePermission):
    """Проверка на текущего пользователя
    """
    def has_permission(self, request, view):
        pk = view.kwargs['pk']
        user = view.queryset.get(pk=pk)
        return request.user == user
