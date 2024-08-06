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
        return request.user._meta.model_name == 'librarian'
