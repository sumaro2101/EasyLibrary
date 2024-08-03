from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.apps import UsersConfig
from users.views import (UserProfileViewAPI,
                         UserCreateProfileAPI,
                         UserUpdateProfileAPI,
                         UserDeleteProfuleAPI,
                         )

app_name = UsersConfig.name

urlpatterns = [
    path('api/token/',
         TokenObtainPairView.as_view(),
         name='token_obtain_pair',
         ),
    path('api/token/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh',
         ),
    path('api/user/create/',
         UserCreateProfileAPI.as_view(),
         name='user_create',
         ),
    path('api/user/<int:pk>/',
         UserProfileViewAPI.as_view(),
         name='user_profile',
         ),
    path('api/user/update/<int:pk>/',
         UserUpdateProfileAPI.as_view(),
         name='user_update',
         ),
    path('api/user/delete/<int:pk>/',
         UserDeleteProfuleAPI.as_view(),
         name='user_delete',
         ),
]
