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
                            Volume,
                            RequestExtension,
                            )


class TestExtension(APITestCase):
    """Тесты модели продления выдач книг
    """

    def setUp(self) -> None:
        user = get_user_model().objects.create(
            username='user',
            email='user@gmail.com',
            phone='+7 (900) 900 2000',
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
        book = Book.objects.create(
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
        book.author.add(author)
        book.genre.add(genre)
        self.order = Order.objects.create(
            book=book,
            tenant=user,
            time_return=date.today() + timedelta(days=30),
        )
        self.librarian = get_user_model().objects.create(
            username='librarian',
            email='librarian@gmail.com',
            phone='+7 (900) 900 2001',
            password='testpassword',
            is_librarian=True,
            is_staff=True,
        )
        self.client.force_authenticate(user)

    def test_open_extension(self):
        """Тест открытия запроса на продление
        """
        url = reverse('library:extension_open',
                      kwargs={'pk': self.order.pk})

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'id': response.data['id'],
            'order': self.order.pk,
            'time_request': response.data['time_request'],
            'receiving': None,
            'time_response': None,
            'solution': 'wait',
        })

    def test_accept_extension(self):
        """Тест принятия продления
        """
        extension = RequestExtension.objects.create(
            order=self.order
        )
        self.client.logout()
        self.client.force_authenticate(self.librarian)
        url = reverse('library:extension_accept',
                      kwargs={'pk': extension.pk},
                      )

        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'id': response.data['id'],
            'order': self.order.pk,
            'time_request': response.data['time_request'],
            'receiving': self.librarian.pk,
            'time_response': response.data['time_response'],
            'solution': 'accept',
        })

    def test_calcel_extension(self):
        """Тест отмены продления
        """
        extension = RequestExtension.objects.create(
            order=self.order
        )
        self.client.logout()
        self.client.force_authenticate(self.librarian)
        url = reverse('library:extension_cancel',
                      kwargs={'pk': extension.pk},
                      )

        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'id': response.data['id'],
            'order': self.order.pk,
            'time_request': response.data['time_request'],
            'receiving': self.librarian.pk,
            'time_response': response.data['time_response'],
            'solution': 'cancel',
        })
