from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

from library.models import Volume


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
            'id': response.data['id'],
            'name': 'fantasy_volume',
        })
        self.assertEqual(Volume.objects.count(), 1)

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
