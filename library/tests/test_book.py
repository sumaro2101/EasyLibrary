from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

from library.models import (Book,
                            Publisher,
                            Genre,
                            Author,
                            )


class TestBook(APITestCase):
    """Тесты модели жанра
    """

    def setUp(self) -> None:
        user = get_user_model().objects.create_user(
            'root',
            'root@gmail.com',
            'password',
            phone='+79006001000',
        )
        self.author = Author.objects.create(first_name='author',
                                       last_name='author_last',
                                       surname='surname',
                                       )
        self.publisher = Publisher.objects.create(
            name='publisher',
            address='new-york',
            url='https://www.publisher.com/',
            email='publisher@gmail.com',
            phone='+79136001000',
        )
        self.genre = Genre.objects.create(
            name_en='fantasy',
            name_ru='Фэнтези',
        )
        self.client.force_authenticate(user)

    def test_create_book(self):
        """Тест создания книги
        """
        url = reverse('library:book_create')
        data = {
            'author': [self.author.pk,],
            'publisher': self.publisher.pk,
            'name': 'book',
            'best_seller': True,
            'volume': True,
            'num_of_volume': 1,
            'age_restriction': 16,
            'count_pages': 300,
            'year_published': 2015,
            'genre': [self.genre.pk,],
            'circulation': 1203,
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {
            'id': response.data['id'],
            'author': [self.author.pk,],
            'publisher': self.publisher.pk,
            'name': 'book',
            'image': None,
            'best_seller': True,
            'volume': True,
            'num_of_volume': 1,
            'age_restriction': 16,
            'count_pages': 300,
            'year_published': 2015,
            'genre': [self.genre.pk,],
            'circulation': 1203,
        })
        self.assertEqual(Book.objects.count(), 1)

    def test_update_book(self):
        """Тест обновления книги
        """
        book = Book.objects.create(
            publisher=self.publisher,
            name='book',
            best_seller=True,
            volume=True,
            num_of_volume=1,
            age_restriction=16,
            count_pages=300,
            year_published=2015,
            circulation=1203,
        )
        book.author.add(self.author)
        book.genre.add(self.genre)
        url = reverse('library:book_update', kwargs={'pk': book.pk})
        data = {
            'name': 'book_update',
        }
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'book_update')

    def test_delete_book(self):
        """Тест удаления издателя
        """
        book = Book.objects.create(
            publisher=self.publisher,
            name='book',
            best_seller=True,
            volume=True,
            num_of_volume=1,
            age_restriction=16,
            count_pages=300,
            year_published=2015,
            circulation=1203,
        )
        book.author.add(self.author)
        book.genre.add(self.genre)
        url = reverse('library:book_delete', kwargs={'pk': book.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)
