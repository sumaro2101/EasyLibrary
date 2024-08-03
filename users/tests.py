from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.exceptions import ErrorDetail

from django.urls import reverse
from django.contrib.auth import get_user_model

from users.validators import ValidatorSetPasswordUser


class TestUserApi(APITestCase):
    """Тесты пользователя
    """

    def test_view_user(self):
        """Тест вывода пользователя
        """
        user = get_user_model().objects.create(username='test',
                                               phone='+7 (900) 900 1000',
                                               email='test@gmail.com',
                                               password='testroot',
                                               )
        self.client.force_authenticate(user=user)
        url = reverse('users:user_profile', kwargs={'pk': user.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': user.pk,
                                         'username': 'test',
                                         'tg_id': None,
                                         'first_name': '',
                                         'last_name': '',
                                         'email': 'test@gmail.com',
                                         'phone': '+79009001000',
                                         'last_login': user.last_login,
                                         'is_staff': False,
                                         'groups': []
                                         })

    def test_create_user(self):
        """Тест создания пользователя
        """
        url = reverse('users:user_create')
        data = {'username': 'test',
                'email': 'test@gmail.com',
                'phone': '+7 (900) 900 1000',
                'password': 'testroot',
                'password_check': 'testroot',
                }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(get_user_model().objects.get().username, 'test')

    def test_create_user_bad_arguments(self):
        """Тест создания пользователя с недостающими аргументами
        """
        url = reverse('users:user_create')
        data = {'email': 'test@gmail.com',
                'password': 'testroot',
                }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(get_user_model().objects.count(), 0)

    def test_create_validate_password(self):
        """Тест валидации не одинаковых паролей
        """
        url = reverse('users:user_create')
        data = {'username': 'test',
                'email': 'test@gmail.com',
                'phone': '+7 (900) 900 1000',
                'password': 'testroot',
                'password_check': 'testrootnotsome',
                }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['non_field_errors'],
            [ErrorDetail(
                string='Пароли не совпадают',
                code='invalid',
                ),
             ],
            )

    def test_create_validate_common_password(self):
        """Тест валидации простого пароля
        """
        url = reverse('users:user_create')
        data = {'username': 'test',
                'email': 'test@gmail.com',
                'phone': '+7 (900) 900 1000',
                'password': '12345678',
                'password_check': '12345678',
                }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['non_field_errors'],
            [ErrorDetail(string='Введённый пароль '
                         'слишком широко распространён.',
                         code='password_too_common',
                         ),
             ],
            )

    def test_update_user(self):
        """Тест изменения пользователя
        """
        user = get_user_model().objects.create(username='test',
                                               phone='+7 (900) 900 1000',
                                               email='test@gmail.com',
                                               password='testroot',
                                               )
        self.client.force_authenticate(user=user)

        url = reverse('users:user_update', kwargs={'pk': user.pk})
        data = {'username': 'change',
                'email': 'change@gmail.com',
                }
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(get_user_model().objects.filter(username='change',
                                                        ).exists())
        self.assertFalse(get_user_model().objects.filter(username='test',
                                                         ).exists())

    def test_change_activity_user(self):
        """Тест изменения активности пользователя
        """
        user = get_user_model().objects.create(username='test',
                                               phone='+7 (900) 900 1000',
                                               email='test@gmail.com',
                                               password='testroot',
                                               )
        self.client.force_authenticate(user=user)
        url = reverse('users:user_delete', kwargs={'pk': user.pk})

        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertFalse(get_user_model().objects.get(username='test',
                                                      ).is_active)

    def test_validator_set_password_user(self):
        """Проверка валидатора для пользователя
        """
        # Проверка на число
        with self.assertRaises(TypeError):
            ValidatorSetPasswordUser(223)

        # Проверка на список с числом
        with self.assertRaises(TypeError):
            ValidatorSetPasswordUser(['str', 223])

        # Проверка списка < 2
        with self.assertRaises(KeyError):
            ValidatorSetPasswordUser(['str',])

        # Проверка списка > 2
        with self.assertRaises(KeyError):
            ValidatorSetPasswordUser(['str', 'str', 'str'])

        validate = ValidatorSetPasswordUser(['first', 'second'])
        # Проверка корректности заполнения
        self.assertEqual(validate.passwords, ['first', 'second'])
        # Проверка корректности проверки правильных аргументов
        self.assertIsNone(validate({'first': 'rootpassword',
                                    'second': 'rootpassword'}))
