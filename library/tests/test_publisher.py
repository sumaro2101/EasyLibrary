from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

from library.models import Publisher


class TestPublisher(APITestCase):
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

    def test_create_publisher(self):
        """Тест создания издателя
        """
        url = reverse('publisher_create')
        data = {
            'name': 'publisher',
            'address': 'new-york',
            'url': 'https://www.publisher.com/',
            'email': 'publisher@gmail.com',
            'phone': '+79136001000',
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {
            'name': 'publisher',
            'address': 'new-york',
            'url': 'https://www.publisher.com/',
            'email': 'publisher@gmail.com',
            'phone': '+79136001000',
        })
        self.assertEqual(Publisher.objects.count(), 1)

    def test_update_publisher(self):
        """Тест обновления издателя
        """
        publisher = Publisher.objects.create(
            name='publisher',
            address='new-york',
            url='https://www.publisher.com/',
            email='publisher@gmail.com',
            phone='+79136001000',
        )
        url = reverse('publisher_update', kwargs={'pk': publisher.pk})
        data = {
            'name': 'publisher_update',
        }
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'publisher_update')

    def test_delete_Publisher(self):
        """Тест удаления издателя
        """
        publisher = Publisher.objects.create(
            name='publisher',
            address='new-york',
            url='https://www.publisher.com/',
            email='publisher@gmail.com',
            phone='+79136001000',
        )
        url = reverse('publisher_delete', kwargs={'pk': publisher.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Publisher.objects.count(), 0)
