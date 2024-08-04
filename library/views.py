from rest_framework import generics

from library.models import (Book,
                            Genre,
                            Author,
                            Publisher,
                            )
from library.serializers import (BookCreateSerializer,
                                 BookRetrieveSerializer,
                                 GenreSerializer,
                                 AuthorSerializer,
                                 PublisherSerializer,
                                 )

# Книга
class BookCreateAPIView(generics.CreateAPIView):
    """Енд поинт создания книги
    """
    serializer_class = BookCreateSerializer
    queryset = Book.objects.get_queryset()
    

class BookUpdateAPIView(generics.UpdateAPIView):
    """Енд поинт обновления книги
    """
    serializer_class = BookCreateSerializer
    queryset = Book.objects.get_queryset()


class BookDeleteAPIView(generics.DestroyAPIView):
    """Енд поинт удаления книги
    """
    queryset = Book.objects.get_queryset()


class BookRetrieveAPIView(generics.RetrieveAPIView):
    """Енд поинт просмотра книги
    """
    serializer_class = BookRetrieveSerializer
    queryset = Book.objects.get_queryset()


class BookListAPIView(generics.ListAPIView):
    """Енд поинт списка книг
    """
    serializer_class = BookRetrieveSerializer
    queryset = Book.objects.get_queryset()

# Автор
class AuthorCreateAPIView(generics.CreateAPIView):
    """Енд поинт создания автора
    """
    serializer_class = AuthorSerializer
    queryset = Author.objects.get_queryset()


class AuthorUpdateAPIView(generics.UpdateAPIView):
    """Енд поинт обновления автора
    """
    serializer_class = AuthorSerializer
    queryset = Author.objects.get_queryset()


class AuthorDeleteAPIView(generics.DestroyAPIView):
    """Енд поинт удаления автора
    """
    queryset = Author.objects.get_queryset()


class AuthorRetrieveAPIView(generics.RetrieveAPIView):
    """Енд поинт просмотра автора
    """
    serializer_class = AuthorSerializer
    queryset = Author.objects.get_queryset()


class AuthorListAPIView(generics.ListAPIView):
    """Енд поинт списка авторов
    """
    serializer_class = AuthorSerializer
    queryset = Author.objects.get_queryset()


# Издатель
class PublisherCreateAPIView(generics.CreateAPIView):
    """Енд поинт создания издателя
    """
    serializer_class = PublisherSerializer
    queryset = Publisher.objects.get_queryset()


class PublisherUpdateAPIView(generics.UpdateAPIView):
    """Енд поинт обновления издателя
    """
    serializer_class = PublisherSerializer
    queryset = Publisher.objects.get_queryset()


class PublisherDeleteAPIView(generics.DestroyAPIView):
    """Енд поинт удаления издателя
    """
    queryset = Publisher.objects.get_queryset()


class PublisherRetrieveAPIView(generics.RetrieveAPIView):
    """Енд поинт просмотра издателя
    """
    serializer_class = PublisherSerializer
    queryset = Publisher.objects.get_queryset()


class PublisherListAPIView(generics.ListAPIView):
    """Енд поинт списка издателей
    """
    serializer_class = PublisherSerializer
    queryset = Publisher.objects.get_queryset()


# Жанр
class GenreCreateAPIView(generics.CreateAPIView):
    """Енд поинт создания жанра
    """
    serializer_class = GenreSerializer
    queryset = Genre.objects.get_queryset()


class GenreUpdateAPIView(generics.UpdateAPIView):
    """Енд поинт обновления жанра
    """
    serializer_class = GenreSerializer
    queryset = Genre.objects.get_queryset()


class GenreDeleteAPIView(generics.DestroyAPIView):
    """Енд поинт удаления жанра
    """
    queryset = Genre.objects.get_queryset()


class GenreRetrieveAPIView(generics.RetrieveAPIView):
    """Енд поинт просмотра жанра
    """
    serializer_class = GenreSerializer
    queryset = Genre.objects.get_queryset()


class GenreListAPIView(generics.ListAPIView):
    """Енд поинт списка жанров
    """
    serializer_class = GenreSerializer
    queryset = Genre.objects.get_queryset()