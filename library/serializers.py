from rest_framework import serializers

from library import models


class BookCreateSerializer(serializers.ModelSerializer):
    """Серилизатор создания книги
    """

    class Meta:
        model = models.Book
        fields = ('__all__',)


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
                  )


class AuthorSerializer(serializers.ModelSerializer):
    """Серилизатор автора
    """

    class Meta:
        model = models.Author
        fields = ('__all__',)


class PublisherSerializer(serializers.ModelSerializer):
    """Серилизатор издателя
    """

    class Meta:
        model = models.Publisher
        fields = ('__all__',)


class GenreSerializer(serializers.ModelSerializer):
    """Серилизатор жанра
    """

    class Meta:
        model = models.Genre
        fields = ('__all__',)
