from django.test import TestCase

from rest_framework.validators import ValidationError

from library.validators import (VolumeValidator,
                                YearValidator,
                                PublishedValidator,
                                )
from library.models import (Book,
                            Genre,
                            Author,
                            Publisher, Volume,
                            )


class TestValidators(TestCase):
    """Тесты валидаторов
    """
    
    def setUp(self) -> None:
        class Serializer:
            class Instance:
                best_seller =True
                circulation = 20
                is_published = True
                year_published = 2017
            instance = Instance
                        
        self.serializer = Serializer

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

    def test_volume_validator(self):
        """Тест валидатора тома
        """
        value1 = {
            'volume': True,
            'num_of_volume': 2,
        }
        value2 = {
            'volume': False,
            'num_of_volume': None,
        }
        validator = VolumeValidator(['volume', 'num_of_volume'])

        self.assertEqual(validator(value1), None)
        self.assertEqual(validator(value2), None)
        
    def test_wrong_value_validator(self):
        """Тест валидатора на указания номера тома без значения тома
        """
        value1 = {
            'volume': True,
            'num_of_volume': None,
        }
        value2 = {
            'volume': False,
            'num_of_volume': 2,
        }
        validator = VolumeValidator(['volume', 'num_of_volume'])

        with self.assertRaises(ValidationError):
            validator(value1)
        with self.assertRaises(ValidationError):
            validator(value2)

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
        volume = Volume.objects.create(
            name='fantasy_volume',
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
        value = {
            'volume': True,
            'num_of_volume': 1,
        }
        validator = VolumeValidator(['volume', 'num_of_volume'])

        with self.assertRaises(ValidationError):
            validator(value)

    def test_published_validator(self):
        """Тест валидатора на значения при публикации
        """
        value = {
            'best_seller': False,
            'circulation': 0,
            'is_published': False,
        }
        validator = PublishedValidator('best_seller', 'circulation', 'is_published')

        self.assertEqual(validator(value, self.serializer), None)

    def test_wrong_values_validator(self):
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

        validator = PublishedValidator('best_seller', 'circulation', 'is_published')

        with self.assertRaises(ValidationError):
            validator(value1, self.serializer)
        with self.assertRaises(ValidationError):
            validator(value2, self.serializer)
        with self.assertRaises(ValidationError):
            validator(value3, self.serializer)
