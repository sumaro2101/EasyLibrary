from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.exceptions import ErrorDetail

from django.urls import reverse
from django.contrib.auth import get_user_model

from users.validators import ValidatorSetPasswordUser
from users.models import Librarian


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


class TestLibrarianAPI(APITestCase):
    """Тесты библиотекаря
    """

    def setUp(self) -> None:
        self.admin = get_user_model().objects.create_superuser(
            'admin',
            'admin@gmail.com',
            'password',
            phone='+79006001000'
        )
        self.client.force_authenticate(user=self.admin)
        
    def test_retrieve_librarian(self):
        """Тест создания библиотекаря
        """
        data = {'username': 'librarian',
                'email': 'librarian@gmail.com',
                'phone': '+7 (900) 900 1000',
                'password': 'testpassword',
                'password_check': 'testpassword',
                }
        url = reverse('users:librarian_create')
        response1 = self.client.post(url, data, format='json')
        url = reverse('users:librarian_profile', kwargs={
            'pk': response1.data['id']
        })
        response2 = self.client.get(url, format='json')

        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertTrue(Librarian.objects.get(
            pk=response1.data['id'],
            ).is_staff)

    def test_create_librarian(self):
        """Тест создания библиотекаря
        """
        data = {'username': 'librarian',
                'email': 'librarian@gmail.com',
                'phone': '+7 (900) 900 1000',
                'password': 'testpassword',
                'password_check': 'testpassword',
                }
        url = reverse('users:librarian_create')
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Librarian.objects.count(), 1)

    def test_update_librarian(self):
        """Тест обновления профиля библиотекаря
        """
        librarian = Librarian.objects.create(
            username='librarian',
            email='librarian@gmail.com',
            phone='+7 (900) 900 1000',
            password='testpassword',
        )
        self.client.logout()
        self.client.force_authenticate(user=librarian)

        url = reverse('users:librarian_update', kwargs={
            'pk': librarian.pk,
            })
        data = {
            'username': 'updated'
        }
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'updated')

    def test_delete_librarian(self):
        """Тест удаления библиотекаря
        """
        librarian = Librarian.objects.create(
            username='librarian',
            email='librarian@gmail.com',
            phone='+7 (900) 900 1000',
            password='testpassword',
        )
        url = reverse('users:librarian_delete', kwargs={
            'pk': librarian.pk,
        })

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Librarian.objects.count(), 1)
        self.assertFalse(Librarian.objects.get(pk=librarian.pk).is_active)
