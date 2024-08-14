from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

from library.models import Genre


class TestGenre(APITestCase):
    """Тесты модели жанра
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

    def test_retrieve_genre(self):
        """Тест вывода жанра
        """
        genre = Genre.objects.create(
            name_en='fantasy',
            name_ru='Фэнтези',
        )
        url = reverse('library:genre_retrieve',
                      kwargs={'pk': genre.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'id': response.data['id'],
            'name_en': 'fantasy',
            'name_ru': 'Фэнтези',
        })

    def test_retrieve_genre_allow_any_permission(self):
        """Тест вывода жанра с всеми правами
        """
        genre = Genre.objects.create(
            name_en='fantasy',
            name_ru='Фэнтези',
        )
        url = reverse('library:genre_retrieve',
                      kwargs={'pk': genre.pk})
        self.client.logout()

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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

    def test_create_genre_permission(self):
        """Тест прав доступа создания жанра
        """
        url = reverse('library:genre_create')
        data = {
            'name_en': 'fantasy',
            'name_ru': 'Фэнтези',
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

    def test_update_genre_permission(self):
        """Тест прав доступа обновления жанра
        """
        genre = Genre.objects.create(
            name_en='fantasy',
            name_ru='Фэнтези',
        )
        url = reverse('library:genre_update', kwargs={'pk': genre.pk})
        data = {
            'name_ru': 'Фэнтези крутое',
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

    def test_delete_genre_permission(self):
        """Тест прав доступа удаления жанра
        """
        genre = Genre.objects.create(
            name_en='fantasy',
            name_ru='Фэнтези',
        )
        url = reverse('library:genre_delete', kwargs={'pk': genre.pk})
        user = get_user_model().objects.create(username='test',
                                               phone='+7 (900) 900 1000',
                                               email='test@gmail.com',
                                               password='testroot',
                                               )
        self.client.logout()
        self.client.force_authenticate(user=user)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
