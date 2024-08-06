from rest_framework import serializers
from rest_framework.fields import get_error_detail
from rest_framework.validators import ValidationError

from django.core.exceptions import ValidationError as DjangoValidationError

from library import models
from library.validators import (YearValidator,
                                PublishedValidator,
                                VolumeValidator,
                                )


class BookCreateSerializer(serializers.ModelSerializer):
    """Серилизатор создания книги
    """

    class Meta:
        model = models.Book
        fields = ('id',
                  'author',
                  'publisher',
                  'name',
                  'image',
                  'best_seller',
                  'volume',
                  'num_of_volume',
                  'age_restriction',
                  'count_pages',
                  'year_published',
                  'genre',
                  'circulation',
                  'is_published',
                  )
        validators = (YearValidator('year_published', 'is_published'),
                      PublishedValidator('best_seller',
                                         'circulation',
                                         'is_published',
                                         ),
                      VolumeValidator('volume',
                                      'num_of_volume',
                                      ),
                     )


class BookRetrieveSerializer(serializers.ModelSerializer):
    """Серилизатор вывода книг
    """

    class Meta:
        model = models.Book
        fields = ('author',
                  'publisher',
                  'name',
                  'image',
                  'best_seller',
                  'volume',
                  'num_of_volume',
                  'age_restriction',
                  'count_pages',
                  'year_published',
                  'genre',
                  'circulation',
                  'is_published',
                  )


class AuthorSerializer(serializers.ModelSerializer):
    """Серилизатор автора
    """

    class Meta:
        model = models.Author
        fields = '__all__'


class PublisherSerializer(serializers.ModelSerializer):
    """Серилизатор издателя
    """

    class Meta:
        model = models.Publisher
        fields = '__all__'


class VolumeSerializer(serializers.ModelSerializer):
    """Серилизатор тома
    """

    class Meta:
        model = models.Volume
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    """Серилизатор жанра
    """

    class Meta:
        model = models.Genre
        fields = '__all__'
