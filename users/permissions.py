from rest_framework.permissions import BasePermission


class IsCurrentUser(BasePermission):
    """Проверка на текущего пользователя
    """
    def has_permission(self, request, view):
        pk = view.kwargs['pk']
        user = view.queryset.get(pk=pk)
        return request.user == user


class IsSuperUser(BasePermission):
    """Проверка прав доступа администратора
    """
    def has_permission(self, request, view):
        return request.user.is_superuser
