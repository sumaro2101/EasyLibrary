from rest_framework import serializers

from library import models
from library.validators import (YearValidator,
                                PublishedValidator,
                                VolumeValidator,
                                )


class PublisherSerializer(serializers.ModelSerializer):
    """Серилизатор издателя
    """

    class Meta:
        model = models.Publisher
        fields = '__all__'


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
    author = serializers.StringRelatedField(many=True)
    publisher = serializers.StringRelatedField()
    volume = serializers.StringRelatedField()
    genre = serializers.StringRelatedField(many=True)

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
    books = serializers.StringRelatedField(many=True,
                                           read_only=True,
                                           source='book_set')

    class Meta:
        model = models.Author
        fields = ('first_name',
                  'last_name',
                  'surname',
                  'portrait',
                  'books',
                  )


class VolumeSerializer(serializers.ModelSerializer):
    """Серилизатор тома
    """
    books = BookRetrieveSerializer(many=True,
                                   read_only=True,
                                   )
    class Meta:
        model = models.Volume
        fields = ('pk',
                  'name',
                  'books',
                  )


class GenreSerializer(serializers.ModelSerializer):
    """Серилизатор жанра
    """

    class Meta:
        model = models.Genre
        fields = '__all__'
