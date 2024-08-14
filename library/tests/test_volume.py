from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

from library.models import Volume


class TestVolume(APITestCase):
    """Тесты модели тома
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

    def test_retrieve_volume(self):
        """Тест вывода тома
        """
        volume = Volume.objects.create(
            name='fantasy_volume',
        )
        url = reverse('library:volume_retrieve',
                      kwargs={'pk': volume.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'pk': response.data['pk'],
            'name': 'fantasy_volume',
            'books': [],
        })

    def test_retrieve_volume_allow_any_permission(self):
        """Тест вывода тома с полными разрешениями
        """
        volume = Volume.objects.create(
            name='fantasy_volume',
        )
        url = reverse('library:volume_retrieve',
                      kwargs={'pk': volume.pk})
        self.client.logout()

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_volume(self):
        """Тест создания тома
        """
        url = reverse('library:volume_create')
        data = {
            'name': 'fantasy_volume',
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {
            'pk': response.data['pk'],
            'name': 'fantasy_volume',
            'books': [],
        })
        self.assertEqual(Volume.objects.count(), 1)

    def test_create_volume_permission(self):
        """Тест прав доступа создания тома
        """
        url = reverse('library:volume_create')
        data = {
            'name': 'fantasy_volume',
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

    def test_update_volume(self):
        """Тест обновления тома
        """
        volume = Volume.objects.create(
            name='fantasy_volume',
        )
        url = reverse('library:volume_update', kwargs={'pk': volume.pk})
        data = {
            'name': 'volume_updated',
        }
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'volume_updated')

    def test_update_volume_permission(self):
        """Тест прав доступа обновления тома
        """
        volume = Volume.objects.create(
            name='fantasy_volume',
        )
        url = reverse('library:volume_update', kwargs={'pk': volume.pk})
        data = {
            'name': 'volume_updated',
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

    def test_delete_volume(self):
        """Тест удаления тома
        """
        volume = Volume.objects.create(
            name='fantasy_volume',
        )
        url = reverse('library:volume_delete', kwargs={'pk': volume.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Volume.objects.count(), 0)

    def test_delete_volume_permission(self):
        """Тест прав доступа удаления тома
        """
        volume = Volume.objects.create(
            name='fantasy_volume',
        )
        url = reverse('library:volume_delete', kwargs={'pk': volume.pk})
        user = get_user_model().objects.create(username='test',
                                               phone='+7 (900) 900 1000',
                                               email='test@gmail.com',
                                               password='testroot',
                                               )
        self.client.logout()
        self.client.force_authenticate(user=user)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
