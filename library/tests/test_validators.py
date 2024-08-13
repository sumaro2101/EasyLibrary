from datetime import date, timedelta
from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.validators import ValidationError
from rest_framework.test import APITestCase

from library.validators import (VolumeValidator,
                                YearValidator,
                                PublishedValidator,
                                OrderRepeatValidator,
                                BookQuantityValidator,
                                ExtensionValidator,
                                SomeUserValidator,
                                ResponseValidator,
                                CountExtensionsValidator,
                                IsActiveOrderValidator,
                                )
from library.models import (Book,
                            Genre,
                            Author, Order,
                            Publisher, RequestExtension,
                            Volume,
                            )


class TestValidators(TestCase):
    """Тесты валидаторов
    """

    def setUp(self) -> None:
        self.volume = Volume.objects.create(
            name='fantasy_volume',
        )

        class Serializer:
            class Instance:
                volume = self.volume
                num_of_volume = 1
                best_seller = True
                circulation = 20
                is_published = True
                year_published = 2017
            instance = Instance

        self.serializer = Serializer

    def test_year_validator_fields(self):
        """Тест валидатора на входящие значения полей
        """
        with self.assertRaises(TypeError):
            YearValidator([], [])

    def test_year_validator(self):
        """Тест валидатора года
        """
        value1 = {
            'year': 2017,
            'is_published': True,
        }
        value2 = {
            'year': 2030,
            'is_published': False,
        }
        validator = YearValidator('year', 'is_published')

        self.assertEqual(validator(value1, self.serializer), None)
        self.assertEqual(validator(value2, self.serializer), None)

    def test_year_wrong_value_validator(self):
        """Тест валидатора года с неправильным значением
        """
        value1 = {
            'year': 1456,
            'is_published': True,
        }
        value2 = {
            'year': 2030,
            'is_published': True,
        }
        validator = YearValidator('year', 'is_published')

        with self.assertRaises(ValidationError):
            validator(value1, self.serializer)

        with self.assertRaises(ValidationError):
            validator(value2, self.serializer)

    def test_volume_validator_fields(self):
        """Тест валидатора на входящие значения полей
        """
        with self.assertRaises(TypeError):
            VolumeValidator([], [])

    def test_volume_validator(self):
        """Тест валидатора тома
        """
        value1 = {
            'volume': self.volume,
            'num_of_volume': 2,
        }
        value2 = {
            'volume': None,
            'num_of_volume': None,
        }
        validator = VolumeValidator('volume', 'num_of_volume')

        self.assertEqual(validator(value1, self.serializer), None)
        self.assertEqual(validator(value2, self.serializer), None)

    def test_wrong_value_validator(self):
        """Тест валидатора на указания номера тома без значения тома
        """
        value1 = {
            'volume': self.volume,
            'num_of_volume': None,
        }
        value2 = {
            'volume': None,
            'num_of_volume': 2,
        }
        validator = VolumeValidator('volume', 'num_of_volume')
        serializer = self.serializer
        serializer.instance = None

        with self.assertRaises(ValidationError):
            validator(value1, serializer)
        with self.assertRaises(ValidationError):
            validator(value2, serializer)

    def test_wrong_value_volume_validator(self):
        """Тест валидатора на не правильные значения тома
        """
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
        genre = Genre.objects.create(
            name_en='fantasy',
            name_ru='Фэнтези',
        )
        book = Book.objects.create(
            publisher=publisher,
            name='book',
            best_seller=True,
            volume=self.volume,
            num_of_volume=2,
            age_restriction=16,
            count_pages=300,
            year_published=2015,
            circulation=1203,
            is_published=True,
        )
        book.author.add(author)
        book.genre.add(genre)
        value = {
            'volume': self.volume,
            'num_of_volume': 2,
        }
        validator = VolumeValidator('volume', 'num_of_volume')

        with self.assertRaises(ValidationError):
            validator(value, self.serializer)

    def test_published_validator_fields(self):
        """Тест валидатора на входящие значения полей
        """
        with self.assertRaises(TypeError):
            PublishedValidator(([], [], []))

    def test_published_validator(self):
        """Тест валидатора на значения при публикации
        """
        value = {
            'best_seller': False,
            'circulation': 0,
            'is_published': False,
        }
        validator = PublishedValidator('best_seller',
                                       'circulation',
                                       'is_published',
                                       )

        self.assertEqual(validator(value, self.serializer), None)

    def test_wrong_values_published_validator(self):
        """Тест на не правильные значения
        """
        value1 = {
            'best_seller': True,
            'circulation': 1000,
            'is_published': False,
        }
        value2 = {
            'best_seller': True,
            'circulation': 0,
            'is_published': False,
        }
        value3 = {
            'best_seller': False,
            'circulation': 0,
            'is_published': True,
        }

        validator = PublishedValidator('best_seller',
                                       'circulation',
                                       'is_published',
                                       )

        with self.assertRaises(ValidationError):
            validator(value1, self.serializer)
        with self.assertRaises(ValidationError):
            validator(value2, self.serializer)
        with self.assertRaises(ValidationError):
            validator(value3, self.serializer)


class TestOrderValidators(APITestCase):
    """Тест валидаторов на выдачу книг
    """
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            username='user',
            email='user@gmail.com',
            phone='+7 (900) 900 2001',
            password='testpassword',
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
        self.book = Book.objects.create(
            publisher=self.publisher,
            name='book',
            best_seller=True,
            volume=self.volume,
            num_of_volume=1,
            age_restriction=16,
            count_pages=300,
            quantity=1,
            year_published=2015,
            circulation=1203,
            is_published=True,
        )
        self.book.author.add(self.author)
        self.book.genre.add(self.genre)

        self.order = Order.objects.create(
            book=self.book,
            tenant=self.user,
            time_return=date.today() + timedelta(days=30),
        )

        class SerializerCreate:
            initial_data = {
                'book': self.book,
                'tenant': self.user,
                'applicant': self.user,
                'order': self.order,
            }

        self.serializer_create = SerializerCreate
        self.client.force_authenticate(self.user)

    def test_order_repeat_validator_fields(self):
        """Тест валидатора на входящие значения полей
        """
        with self.assertRaises(TypeError):
            OrderRepeatValidator([])

    def test_validator_repeat_book_in_order(self):
        """Тест валидатора на повторении выданной книги
        """
        data = {
            'book': self.book,
            'tenant': self.user,
        }
        validator = OrderRepeatValidator('book')

        with self.assertRaises(ValidationError):
            validator(data, self.serializer_create)

    def test_validator_repeat_non_repeat_book(self):
        """Тест валидатора на правильныe значения
        """
        book = Book.objects.create(
            publisher=self.publisher,
            name='book',
            best_seller=True,
            volume=self.volume,
            num_of_volume=2,
            age_restriction=16,
            count_pages=300,
            year_published=2015,
            circulation=1203,
            is_published=True,
        )
        book.author.add(self.author)
        book.genre.add(self.genre)

        data = {
            'book': book,
        }

        class SerializerCreate:
            initial_data = {
                'book': book,
                'tenant': self.user
            }

        serializer_create = SerializerCreate
        validator = OrderRepeatValidator('book')

        self.assertEqual(validator(data, serializer_create), None)

    def test_order_quantity_validator_fields(self):
        """Тест валидатора на входящие значения полей
        """
        with self.assertRaises(TypeError):
            BookQuantityValidator([])

    def test_validator_quantity_book(self):
        """Валидатор количества книг
        """
        user = get_user_model().objects.create(
            username='user1',
            email='user1@gmail.com',
            phone='+7 (900) 900 2021',
            password='testpassword',
        )
        self.client.logout()
        self.client.force_authenticate(user)
        data = {
            'book': self.book
        }
        validator = BookQuantityValidator('book')

        with self.assertRaises(ValidationError):
            validator(data, self.serializer_create)

    def test_pass_validator_quantity_book(self):
        """Проверка валидатора на правильные значения
        """
        book = Book.objects.create(
            publisher=self.publisher,
            name='book',
            best_seller=True,
            volume=self.volume,
            num_of_volume=2,
            age_restriction=16,
            count_pages=300,
            quantity=1,
            year_published=2015,
            circulation=1203,
            is_published=True,
        )
        self.book.author.add(self.author)
        self.book.genre.add(self.genre)
        data = {
            'book': book
        }

        class SerializerCreate:
            initial_data = {
                'book': book,
                'tenant': self.user
            }

        serializer_create = SerializerCreate

        validator = BookQuantityValidator('book')
        self.assertIsNone(validator(data, serializer_create))

    def test_extension_validator_fields(self):
        """Тест валидатора на входящие значения полей
        """
        with self.assertRaises(TypeError):
            OrderRepeatValidator([])

    def test_extension_validator(self):
        """Тест валидатора на повторение запроса
        на продление той же книги
        """
        RequestExtension.objects.create(
            order=self.order,
            applicant=self.user
        )

        class Serializer:
            initial_data = {
                'order': self.order,
                'applicant': self.user
            }

        serializer = Serializer
        data = {}
        validator = ExtensionValidator('order')

        with self.assertRaises(ValidationError):
            validator(data, serializer)

    def test_extension_pass_validator(self):
        """Тест валидатора на правильные значения
        """
        data = {}

        class Serializer:
            initial_data = {
                'order': self.order,
                'applicant': self.user
            }

        serializer = Serializer
        validator = ExtensionValidator('order')

        self.assertIsNone(validator(data, serializer))

    def test_some_user_validator_fields(self):
        """Тест валидатора на входящие значения полей
        """
        with self.assertRaises(TypeError):
            SomeUserValidator([])

    def test_some_user_validator(self):
        """Тест валидатора на одного и того же пользователя
        """
        data = {
            'order': self.order
        }
        validator = SomeUserValidator('order')
        user = get_user_model().objects.create(
            username='user1',
            email='user1@gmail.com',
            phone='+7 (900) 900 2021',
            password='testpassword',
        )
        self.client.logout()
        self.client.force_authenticate(user)

        class Serializer:
            initial_data = {
                'order': self.order,
                'applicant': user
            }

        serializer = Serializer

        with self.assertRaises(ValidationError):
            validator(data, serializer)

    def test_some_user_validator1(self):
        """Тест валидатора на правильные значения
        """
        data = {
            'order': self.order
        }
        validator = SomeUserValidator('order')

        self.assertIsNone(validator(data, self.serializer_create))

    def test_response_validator_fields(self):
        """Тест валидатора на входящие значения полей
        """
        with self.assertRaises(TypeError):
            ResponseValidator([])

    def test_response_validator(self):
        """Тест валидатора на проверку того что
        запрос обработан
        """
        extension = RequestExtension.objects.create(
            order=self.order,
            applicant=self.user,
            solution='cancel',
        )

        class Serializer:
            instance = extension

        serializer = Serializer
        data = {}
        validator = ResponseValidator('solution')

        with self.assertRaises(ValidationError):
            validator(data, serializer)

    def test_response_validator_pass(self):
        """Тест валидатора с правильными значениями
        """
        extension = RequestExtension.objects.create(
            order=self.order,
            applicant=self.user,
        )

        class Serializer:
            instance = extension

        serializer = Serializer
        data = {}
        validator = ResponseValidator('solution')

        self.assertIsNone(validator(data, serializer))

    def test_count_extensions_validator(self):
        """Тест валидатора на количество продлений
        """
        order = Order.objects.create(
            book=self.book,
            tenant=self.user,
            time_return=date.today() + timedelta(days=30),
            count_extensions=2,
        )
        data = {}

        class Serializer:
            initial_data = {
                'order': order,
                'applicant': self.user
            }

        serializer = Serializer
        validator = CountExtensionsValidator('order')

        with self.assertRaises(ValidationError):
            validator(data, serializer)

    def test_is_active_order_validator(self):
        """Тест валидатора на проверку того что
        данная книга еще не была возвращена
        """
        order = Order.objects.create(
            book=self.book,
            tenant=self.user,
            time_return=date.today() + timedelta(days=30),
            status='end',
        )

        class Serializer:
            initial_data = {
                'order': order,
                'applicant': self.user
            }

        serializer = Serializer
        data = {}
        validator = IsActiveOrderValidator('order')

        with self.assertRaises(ValidationError):
            validator(data, serializer)

    def test_is_active_order_validator_pass(self):
        """Тест валидатора на правильные значения
        """
        order = Order.objects.create(
            book=self.book,
            tenant=self.user,
            time_return=date.today() + timedelta(days=30),
        )

        class Serializer:
            initial_data = {
                'order': order,
                'applicant': self.user
            }
        serializer = Serializer

        data = {}
        validator = IsActiveOrderValidator('order')

        self.assertIsNone(validator(data, serializer))
