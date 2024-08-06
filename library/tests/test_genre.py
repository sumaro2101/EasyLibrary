from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

from library.models import Genre


class TestGenre(APITestCase):
    """Тесты модели жанра
    """

    def setUp(self) -> None:
        user = get_user_model().objects.create_user(
            'root',
            'root@gmail.com',
            'password',
            phone='+79006001000',
        )
        self.client.force_authenticate(user)

    def test_create_genre(self):
        """Тест создания жанра
        """
        url = reverse('library:genre_create')
        data = {
            'name_en': 'fantasy',
            'name_ru': 'Фэнтези',
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {
            'id': response.data['id'],
            'name_en': 'fantasy',
            'name_ru': 'Фэнтези',
        })
        self.assertEqual(Genre.objects.count(), 1)

    def test_update_genre(self):
        """Тест обновления жанра
        """
        genre = Genre.objects.create(
            name_en='fantasy',
            name_ru='Фэнтези',
        )
        url = reverse('library:genre_update', kwargs={'pk': genre.pk})
        data = {
            'name_ru': 'Фэнтези крутое',
        }
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name_ru'], 'Фэнтези крутое')

    def test_delete_genre(self):
        """Тест удаления жанра
        """
        genre = Genre.objects.create(
            name_en='fantasy',
            name_ru='Фэнтези',
        )
        url = reverse('library:genre_delete', kwargs={'pk': genre.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Genre.objects.count(), 0)
