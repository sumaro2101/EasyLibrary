from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

from library.models import Publisher


class TestPublisher(APITestCase):
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

    def test_retrieve_publisher(self):
        """Тест вывода издателя
        """
        publisher = Publisher.objects.create(
            name='publisher',
            address='new-york',
            url='https://www.publisher.com/',
            email='publisher@gmail.com',
            phone='+79136001000',
        )
        url = reverse('library:publisher_retrieve',
                      kwargs={'pk': publisher.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'id': response.data['id'],
            'name': 'publisher',
            'address': 'new-york',
            'url': 'https://www.publisher.com/',
            'email': 'publisher@gmail.com',
            'phone': '+79136001000',
        })

    def test_retrieve_published_allow_any_permission(self):
        """Тест вывода издателя со всеми правами
        """
        publisher = Publisher.objects.create(
            name='publisher',
            address='new-york',
            url='https://www.publisher.com/',
            email='publisher@gmail.com',
            phone='+79136001000',
        )
        url = reverse('library:publisher_retrieve',
                      kwargs={'pk': publisher.pk})
        self.client.logout()

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_publisher(self):
        """Тест создания издателя
        """
        url = reverse('library:publisher_create')
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
            'id': response.data['id'],
            'name': 'publisher',
            'address': 'new-york',
            'url': 'https://www.publisher.com/',
            'email': 'publisher@gmail.com',
            'phone': '+79136001000',
        })
        self.assertEqual(Publisher.objects.count(), 1)

    def test_create_publisher_permission(self):
        """Тест защиты прав доступа создания издателя
        """
        url = reverse('library:publisher_create')
        data = {
            'name': 'publisher',
            'address': 'new-york',
            'url': 'https://www.publisher.com/',
            'email': 'publisher@gmail.com',
            'phone': '+79136001000',
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
        url = reverse('library:publisher_update', kwargs={'pk': publisher.pk})
        data = {
            'name': 'publisher_update',
        }
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'publisher_update')

    def test_update_publisher_permission(self):
        """Тест защиты прав доступа обновления
        """
        publisher = Publisher.objects.create(
            name='publisher',
            address='new-york',
            url='https://www.publisher.com/',
            email='publisher@gmail.com',
            phone='+79136001000',
        )
        url = reverse('library:publisher_update', kwargs={'pk': publisher.pk})
        data = {
            'name': 'publisher_update',
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

    def test_delete_publisher(self):
        """Тест удаления издателя
        """
        publisher = Publisher.objects.create(
            name='publisher',
            address='new-york',
            url='https://www.publisher.com/',
            email='publisher@gmail.com',
            phone='+79136001000',
        )
        url = reverse('library:publisher_delete', kwargs={'pk': publisher.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Publisher.objects.count(), 0)

    def test_delete_publisher_permission(self):
        """Тест защиты прав доступа удаления
        """
        publisher = Publisher.objects.create(
            name='publisher',
            address='new-york',
            url='https://www.publisher.com/',
            email='publisher@gmail.com',
            phone='+79136001000',
        )
        url = reverse('library:publisher_delete', kwargs={'pk': publisher.pk})
        user = get_user_model().objects.create(username='test',
                                               phone='+7 (900) 900 1000',
                                               email='test@gmail.com',
                                               password='testroot',
                                               )
        self.client.logout()
        self.client.force_authenticate(user=user)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
