from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

from library.models import (Book,
                            Publisher,
                            Genre,
                            Author, Volume,
                            )


class TestBook(APITestCase):
    """Тесты модели книги
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
        self.volume = Volume.objects.create(
            name='fantasy_volume',
        )
        self.genre = Genre.objects.create(
            name_en='fantasy',
            name_ru='Фэнтези',
        )
        self.client.force_authenticate(librarian)

    def test_retrieve_book(self):
        """Тест просмотра книги
        """
        book = Book.objects.create(
            publisher=self.publisher,
            name='book',
            best_seller=True,
            volume=self.volume,
            num_of_volume=1,
            age_restriction=16,
            count_pages=300,
            year_published=2015,
            circulation=1203,
            is_published=True,
        )
        book.author.add(self.author)
        book.genre.add(self.genre)
        url = reverse('library:book_retrieve', kwargs={'pk': book.pk})

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'author': ['author_last author'],
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
            'is_published': True,
        })

    def test_retrieve_book_permissons_allow_any(self):
        """Тест просмотра книги для любого пользователя
        """
        book = Book.objects.create(
            publisher=self.publisher,
            name='book',
            best_seller=True,
            volume=self.volume,
            num_of_volume=1,
            age_restriction=16,
            count_pages=300,
            year_published=2015,
            circulation=1203,
            is_published=True,
        )
        book.author.add(self.author)
        book.genre.add(self.genre)
        url = reverse('library:book_retrieve', kwargs={'pk': book.pk})
        self.client.logout()

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_book(self):
        """Тест создания книги
        """
        url = reverse('library:book_create')
        data = {
            'author': [self.author.pk,],
            'publisher': self.publisher.pk,
            'name': 'book',
            'best_seller': True,
            'volume': self.volume.pk,
            'num_of_volume': 1,
            'age_restriction': 16,
            'count_pages': 300,
            'year_published': 2015,
            'genre': [self.genre.pk,],
            'circulation': 1203,
            'is_published': True,
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(response.data, {
            'id': response.data['id'],
            'author': [self.author.pk,],
            'publisher': self.publisher.pk,
            'name': 'book',
            'image': None,
            'best_seller': True,
            'volume': self.volume.pk,
            'num_of_volume': 1,
            'age_restriction': 16,
            'count_pages': 300,
            'year_published': 2015,
            'genre': [self.genre.pk,],
            'circulation': 1203,
            'is_published': True,
        })
        self.assertEqual(Book.objects.count(), 1)

    def test_permission_create_book(self):
        """Тест защиты доступа для книги
        """
        url = reverse('library:book_create')
        data = {
            'author': [self.author.pk,],
            'publisher': self.publisher.pk,
            'name': 'book',
            'best_seller': True,
            'volume': self.volume.pk,
            'num_of_volume': 1,
            'age_restriction': 16,
            'count_pages': 300,
            'year_published': 2015,
            'genre': [self.genre.pk,],
            'circulation': 1203,
            'is_published': True,
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

    def test_update_book(self):
        """Тест обновления книги
        """
        book = Book.objects.create(
            publisher=self.publisher,
            name='book',
            best_seller=True,
            volume=self.volume,
            num_of_volume=1,
            age_restriction=16,
            count_pages=300,
            year_published=2015,
            circulation=1203,
            is_published=True,
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

    def test_permission_update_book(self):
        """Тест защиты доступа для книги
        """
        book = Book.objects.create(
            publisher=self.publisher,
            name='book',
            best_seller=True,
            volume=self.volume,
            num_of_volume=1,
            age_restriction=16,
            count_pages=300,
            year_published=2015,
            circulation=1203,
            is_published=True,
        )
        book.author.add(self.author)
        book.genre.add(self.genre)
        url = reverse('library:book_update', kwargs={'pk': book.pk})
        data = {
            'name': 'book_update',
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

    def test_update_book_wrong_values(self):
        """Тест обновления книги с не правильными значениями
        """
        book = Book.objects.create(
            publisher=self.publisher,
            name='book',
            best_seller=True,
            volume=self.volume,
            num_of_volume=1,
            age_restriction=16,
            count_pages=300,
            year_published=2015,
            circulation=1203,
            is_published=True
        )
        book.author.add(self.author)
        book.genre.add(self.genre)
        url = reverse('library:book_update', kwargs={'pk': book.pk})
        data1 = {
            'circulation': 0,
        }
        data2 = {
            'volume': None,
        }
        data3 = {
            'is_published': False,
        }
        data4 = {
            'year_published': 2030,
        }
        data5 = {
            'num_of_volume': 0,
        }
        response1 = self.client.patch(url, data1, format='json')
        response2 = self.client.patch(url, data2, format='json')
        response3 = self.client.patch(url, data3, format='json')
        response4 = self.client.patch(url, data4, format='json')
        response5 = self.client.patch(url, data5, format='json')

        self.assertEqual(response1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response4.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response5.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_book(self):
        """Тест удаления книги
        """
        book = Book.objects.create(
            publisher=self.publisher,
            name='book',
            best_seller=True,
            volume=self.volume,
            num_of_volume=1,
            age_restriction=16,
            count_pages=300,
            year_published=2015,
            circulation=1203,
            is_published=True
        )
        book.author.add(self.author)
        book.genre.add(self.genre)
        url = reverse('library:book_delete', kwargs={'pk': book.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_permission_book_delete(self):
        """Тест доступа защиты книги
        """
        book = Book.objects.create(
            publisher=self.publisher,
            name='book',
            best_seller=True,
            volume=self.volume,
            num_of_volume=1,
            age_restriction=16,
            count_pages=300,
            year_published=2015,
            circulation=1203,
            is_published=True
        )
        book.author.add(self.author)
        book.genre.add(self.genre)
        url = reverse('library:book_delete', kwargs={'pk': book.pk})
        user = get_user_model().objects.create(username='test',
                                               phone='+7 (900) 900 1000',
                                               email='test@gmail.com',
                                               password='testroot',
                                               )
        self.client.logout()
        self.client.force_authenticate(user=user)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
