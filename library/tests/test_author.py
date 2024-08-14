from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

from library.models import Author


class TestAuthor(APITestCase):
    """Тесты модели автора
    """

    def setUp(self) -> None:
        librarian = get_user_model().objects.create(
            username='librarian',
            email='librarian@gmail.com',
            phone='+7 (900) 900 2000',
            password='testpassword',
            is_librarian=True,
            is_staff=True,
        )
        self.client.force_authenticate(librarian)

    def test_retrieve_author(self):
        """Тест просмотра автора
        """
        author = Author.objects.create(first_name='author',
                                       last_name='author_last',
                                       surname='surname',
                                       )
        url = reverse('library:author_retrieve', kwargs={'pk': author.pk})
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'pk': author.pk,
            'first_name': 'author',
            'last_name': 'author_last',
            'surname': 'surname',
            'portrait': None,
            'books': [],
            'count_books': 0,
        })

    def test_retrieve_author_allow_any_permission(self):
        """Тест просмотра автора с полным доступом
        """
        author = Author.objects.create(first_name='author',
                                       last_name='author_last',
                                       surname='surname',
                                       )
        url = reverse('library:author_retrieve', kwargs={'pk': author.pk})
        self.client.logout()
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_author(self):
        """Тест создания автора
        """
        url = reverse('library:author_create')
        data = {
            'first_name': 'author',
            'last_name': 'author_last',
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {
            'pk': response.data['pk'],
            'first_name': 'author',
            'last_name': 'author_last',
            'surname': None,
            'portrait': None,
            'books': [],
            'count_books': 0,
        })
        self.assertEqual(Author.objects.count(), 1)

    def test_permission_create_author(self):
        """Тест защиты прав доступа автора
        """
        url = reverse('library:author_create')
        data = {
            'first_name': 'author',
            'last_name': 'author_last',
        }
        user = get_user_model().objects.create(username='test',
                                               phone='+7 (900) 900 1000',
                                               email='test@gmail.com',
                                               password='testroot',
                                               )
        self.client.logout()
        self.client.force_authenticate(user=user)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_author(self):
        """Тест обновления автора
        """
        author = Author.objects.create(first_name='author',
                                       last_name='author_last',
                                       surname='surname',
                                       )
        url = reverse('library:author_update', kwargs={'pk': author.pk})
        data = {
            'first_name': 'changed_name',
        }
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'changed_name')

    def test_permission_update_author(self):
        """Тест защиты прав доступа обновления автора
        """
        author = Author.objects.create(first_name='author',
                                       last_name='author_last',
                                       surname='surname',
                                       )
        url = reverse('library:author_update', kwargs={'pk': author.pk})
        data = {
            'first_name': 'changed_name',
        }
        user = get_user_model().objects.create(username='test',
                                               phone='+7 (900) 900 1000',
                                               email='test@gmail.com',
                                               password='testroot',
                                               )
        self.client.logout()
        self.client.force_authenticate(user=user)
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_author(self):
        """Тест удаления автора
        """
        author = Author.objects.create(first_name='author',
                                       last_name='author_last',
                                       surname='surname',
                                       )
        url = reverse('library:author_delete', kwargs={'pk': author.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Author.objects.count(), 0)

    def test_permission_datele_author(self):
        """Тест защиты прав доступа удаления автора
        """
        author = Author.objects.create(first_name='author',
                                       last_name='author_last',
                                       surname='surname',
                                       )
        url = reverse('library:author_delete', kwargs={'pk': author.pk})
        user = get_user_model().objects.create(username='test',
                                               phone='+7 (900) 900 1000',
                                               email='test@gmail.com',
                                               password='testroot',
                                               )
        self.client.logout()
        self.client.force_authenticate(user=user)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
