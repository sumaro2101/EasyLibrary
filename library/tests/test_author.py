from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

from library.models import Author


class TestAuthor(APITestCase):
    """Тесты модели автора
    """

    def setUp(self) -> None:
        user = get_user_model().objects.create_user(
            'root',
            'root@gmail.com',
            'password',
            phone='+79006001000',
        )
        self.client.force_authenticate(user)

    def test_create_author(self):
        """Тест создания автора
        """
        url = reverse('author_create')
        data = {
            'first_name': 'author',
            'last_name': 'author_last',
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {
            'first_name': 'author',
            'last_name': 'author_last',
            'surname': None,
            'portrait': None,
        })
        self.assertEqual(Author.objects.count(), 1)

    def test_update_author(self):
        """Тест обновления автора
        """
        author = Author.objects.create(first_name='author',
                                       last_name='author_last',
                                       surname='surname',
                                       )
        url = reverse('author_update', kwargs={'pk': author.pk})
        data = {
            'first_name': 'changed_name',
        }
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'changed_name')

    def test_delete_author(self):
        """Тест удаления автора
        """
        author = Author.objects.create(first_name='author',
                                       last_name='author_last',
                                       surname='surname',
                                       )
        url = reverse('author_delete', kwargs={'pk': author.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Author.objects.count(), 0)
