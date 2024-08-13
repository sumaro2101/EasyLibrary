from datetime import timedelta, date

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

from library.models import (Author,
                            Book,
                            Genre,
                            Order,
                            Publisher,
                            RequestExtension,
                            Volume,
                            )


class TestOrder(APITestCase):
    """Тесты модели заказа книг на выдачу
    """

    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            username='user',
            email='user@gmail.com',
            phone='+7 (900) 900 2001',
            password='testpassword',
            is_librarian=True,
            is_staff=True,
        )
        author = Author.objects.create(first_name='author',
                                       last_name='author_last',
                                       surname='surname',
                                       )
        publisher = Publisher.objects.create(
            name='publisher',
            address='new-york',
            url='https://www.publisher.com/',
            email='publisher@gmail.com',
            phone='+79136001000',
        )
        volume = Volume.objects.create(
            name='fantasy_volume',
        )
        genre = Genre.objects.create(
            name_en='fantasy',
            name_ru='Фэнтези',
        )
        self.book = Book.objects.create(
            publisher=publisher,
            name='book',
            best_seller=True,
            volume=volume,
            num_of_volume=1,
            age_restriction=16,
            count_pages=300,
            year_published=2015,
            circulation=1203,
            is_published=True,
        )
        self.book.author.add(author)
        self.book.genre.add(genre)
        self.client.force_authenticate(self.user)

    def test_retrieve_order(self):
        """Тест вывода выдачи книги
        """
        order = Order.objects.create(
            book=self.book,
            tenant=self.user,
            time_return=date.today() + timedelta(days=30),
        )
        url = reverse('library:order_retrieve',
                      kwargs={'pk': order.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'id': response.data['id'],
            'book': {'author': ['author_last author'],
                     'publisher': 'publisher',
                     'name': 'book',
                     'image': None,
                     'best_seller': True,
                     'volume': 'fantasy_volume',
                     'num_of_volume': 1,
                     'age_restriction': 16,
                     'count_pages': 300,
                     'year_published': 2015,
                     'genre': ['Фэнтези'],
                     'circulation': 1203,
                     'is_published': True},
            'count_extensions': 0,
            'time_order': response.data['time_order'],
            'time_return': response.data['time_return'],
            'status': 'active',
            'tenant': self.user.pk,
        })

    def test_retrieve_order_permission(self):
        """Тест вывода выдачи с правами доступа
        библеотекаря
        """
        order = Order.objects.create(
            book=self.book,
            tenant=self.user,
            time_return=date.today() + timedelta(days=30),
        )
        url = reverse('library:order_retrieve',
                      kwargs={'pk': order.pk})
        self.client.logout()
        librarian = get_user_model().objects.create(
            username='librarian',
            email='librarian@gmail.com',
            phone='+7 (900) 900 2000',
            password='testpassword',
            is_librarian=True,
            is_staff=True,
        )
        self.client.force_authenticate(librarian)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_open_order(self):
        """Тест открытия выдачи книги
        """
        url = reverse('library:order_open',
                      kwargs={'pk': self.book.pk})
        data = {}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {
            'id': response.data['id'],
            'count_extensions': 0,
            'time_order': response.data['time_order'],
            'time_return': response.data['time_return'],
            'status': 'active',
            'book': self.book.pk,
            'tenant': self.user.pk,
        })
        self.assertEqual(Order.objects.count(), 1)

    def test_open_some_order(self):
        """Тест выдачи одной и той же книги
        """
        url = reverse('library:order_open',
                      kwargs={'pk': self.book.pk})
        data = {}
        self.client.post(url, data, format='json')
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_open_order_permission(self):
        """Тест прав доступа выдачи книги
        """
        url = reverse('library:order_open',
                      kwargs={'pk': self.book.pk})
        data = {}

        self.client.logout()
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_extens_accept_order(self):
        """Тест продления времени выдачи
        """
        url_order = reverse('library:order_open',
                            kwargs={'pk': self.book.pk})
        response_order = self.client.post(url_order)
        url_extension = reverse('library:extension_open',
                                kwargs={'pk': response_order.data['id']})
        response_extension = self.client.post(url_extension)
        url = reverse('library:extension_accept',
                      kwargs={'pk': response_extension.data['id']})
        self.client.logout()
        librarian = get_user_model().objects.create(
            username='librarian',
            email='librarian@gmail.com',
            phone='+7 (900) 900 2000',
            password='testpassword',
            is_librarian=True,
            is_staff=True,
        )
        self.client.force_authenticate(librarian)
        response = self.client.patch(url, format='json')
        order = Order.objects.get(book=self.book)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Продление происходит с текущей даты
        self.assertEqual(order.time_return,
                         order.time_order + timedelta(days=14))
        self.assertEqual(order.count_extensions, 1)

    def test_extens_cancel_order(self):
        """Тест отказа от продления
        """
        order = Order.objects.create(
            book=self.book,
            tenant=self.user,
            time_return=date.today() + timedelta(days=30),
        )
        extension = RequestExtension.objects.create(
            order=order
        )
        url = reverse('library:extension_cancel',
                      kwargs={'pk': extension.pk})
        self.client.logout()
        librarian = get_user_model().objects.create(
            username='librarian',
            email='librarian@gmail.com',
            phone='+7 (900) 900 2000',
            password='testpassword',
            is_librarian=True,
            is_staff=True,
        )
        self.client.force_authenticate(librarian)
        response = self.client.patch(url, format='json')
        order = Order.objects.get(book=self.book)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(order.time_return,
                         order.time_order + timedelta(days=30))
        self.assertEqual(order.count_extensions, 0)

    def test_close_order(self):
        """Тест закрытия выдачи книги
        """
        url_order = reverse('library:order_open',
                            kwargs={'pk': self.book.pk})
        response_order = self.client.post(url_order)
        url = reverse('library:order_close',
                      kwargs={'pk': response_order.data['id']})
        self.client.logout()
        librarian = get_user_model().objects.create(
            username='librarian',
            email='librarian@gmail.com',
            phone='+7 (900) 900 2000',
            password='testpassword',
            is_librarian=True,
            is_staff=True,
        )
        self.client.force_authenticate(librarian)
        response = self.client.delete(url, format='json')
        order = Order.objects.get(book=self.book)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(order.status, 'end')
