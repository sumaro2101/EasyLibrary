from rest_framework import generics
from rest_framework import permissions

from library.models import (Book,
                            Genre,
                            Author,
                            Publisher, Volume,
                            )
from library.serializers import (BookCreateSerializer,
                                 BookRetrieveSerializer,
                                 GenreSerializer,
                                 AuthorSerializer,
                                 PublisherSerializer,
                                 VolumeSerializer,
                                 )
from library.permissions import IsLibrarian, IsSuperUser


# Книга
class BookCreateAPIView(generics.CreateAPIView):
    """Енд поинт создания книги
    """
    serializer_class = BookCreateSerializer
    queryset = Book.objects.get_queryset()
    permission_classes = [permissions.IsAuthenticated & 
                          IsSuperUser | IsLibrarian]
    

class BookUpdateAPIView(generics.UpdateAPIView):
    """Енд поинт обновления книги
    """
    serializer_class = BookCreateSerializer
    queryset = Book.objects.get_queryset()
    permission_classes = [permissions.IsAuthenticated & 
                          IsSuperUser | IsLibrarian]


class BookDeleteAPIView(generics.DestroyAPIView):
    """Енд поинт удаления книги
    """
    queryset = Book.objects.get_queryset()
    permission_classes = [permissions.IsAuthenticated & 
                          IsSuperUser | IsLibrarian]


class BookRetrieveAPIView(generics.RetrieveAPIView):
    """Енд поинт просмотра книги
    """
    serializer_class = BookRetrieveSerializer
    queryset = Book.objects.get_queryset().select_related(
        'publisher',
        'volume',
        ).prefetch_related(
            'author',
            'genre',
            )
    permission_classes = [permissions.AllowAny]


class BookListAPIView(generics.ListAPIView):
    """Енд поинт списка книг
    """
    serializer_class = BookRetrieveSerializer
    queryset = Book.objects.get_queryset().order_by('name').select_related(
        'publisher',
        'volume',
        ).prefetch_related(
            'author',
            'genre',
            )
    permission_classes = [permissions.AllowAny]


# Автор
class AuthorCreateAPIView(generics.CreateAPIView):
    """Енд поинт создания автора
    """
    serializer_class = AuthorSerializer
    queryset = Author.objects.get_queryset()
    permission_classes = [permissions.IsAuthenticated & 
                          IsSuperUser | IsLibrarian]


class AuthorUpdateAPIView(generics.UpdateAPIView):
    """Енд поинт обновления автора
    """
    serializer_class = AuthorSerializer
    queryset = Author.objects.get_queryset()
    permission_classes = [permissions.IsAuthenticated & 
                          IsSuperUser | IsLibrarian]


class AuthorDeleteAPIView(generics.DestroyAPIView):
    """Енд поинт удаления автора
    """
    queryset = Author.objects.get_queryset()
    permission_classes = [permissions.IsAuthenticated & 
                          IsSuperUser | IsLibrarian]


class AuthorRetrieveAPIView(generics.RetrieveAPIView):
    """Енд поинт просмотра автора
    """
    serializer_class = AuthorSerializer
    queryset = Author.objects.get_queryset()
    permission_classes = [permissions.AllowAny]


class AuthorListAPIView(generics.ListAPIView):
    """Енд поинт списка авторов
    """
    serializer_class = AuthorSerializer
    queryset = Author.objects.get_queryset()
    permission_classes = [permissions.AllowAny]


# Издатель
class PublisherCreateAPIView(generics.CreateAPIView):
    """Енд поинт создания издателя
    """
    serializer_class = PublisherSerializer
    queryset = Publisher.objects.get_queryset()
    permission_classes = [permissions.IsAuthenticated & 
                          IsSuperUser | IsLibrarian]


class PublisherUpdateAPIView(generics.UpdateAPIView):
    """Енд поинт обновления издателя
    """
    serializer_class = PublisherSerializer
    queryset = Publisher.objects.get_queryset()
    permission_classes = [permissions.IsAuthenticated & 
                          IsSuperUser | IsLibrarian]


class PublisherDeleteAPIView(generics.DestroyAPIView):
    """Енд поинт удаления издателя
    """
    queryset = Publisher.objects.get_queryset()
    permission_classes = [permissions.IsAuthenticated & 
                          IsSuperUser | IsLibrarian]


class PublisherRetrieveAPIView(generics.RetrieveAPIView):
    """Енд поинт просмотра издателя
    """
    serializer_class = PublisherSerializer
    queryset = Publisher.objects.get_queryset()
    permission_classes = [permissions.AllowAny]


class PublisherListAPIView(generics.ListAPIView):
    """Енд поинт списка издателей
    """
    serializer_class = PublisherSerializer
    queryset = Publisher.objects.get_queryset()
    permission_classes = [permissions.AllowAny]


# Том
class VolumeCreateAPIView(generics.CreateAPIView):
    """Енд поинт создания тома
    """
    serializer_class = VolumeSerializer
    queryset = Volume.objects.get_queryset()
    permission_classes = [permissions.IsAuthenticated & 
                          IsSuperUser | IsLibrarian]


class VolumeUpdateAPIView(generics.UpdateAPIView):
    """Енд поинт обновления тома
    """
    serializer_class = VolumeSerializer
    queryset = Volume.objects.get_queryset()
    permission_classes = [permissions.IsAuthenticated & 
                          IsSuperUser | IsLibrarian]


class VolumeDeleteAPIView(generics.DestroyAPIView):
    """Енд поинт удаления тома
    """
    queryset = Volume.objects.get_queryset()
    permission_classes = [permissions.IsAuthenticated & 
                          IsSuperUser | IsLibrarian]


class VolumeRetrieveAPIView(generics.RetrieveAPIView):
    """Енд поинт просмотра тома
    """
    serializer_class = VolumeSerializer
    queryset = Volume.objects.get_queryset()
    permission_classes = [permissions.AllowAny]


class VolumeListAPIView(generics.ListAPIView):
    """Енд поинт списка томов
    """
    serializer_class = VolumeSerializer
    queryset = Volume.objects.get_queryset().order_by('name')
    permission_classes = [permissions.AllowAny]


# Жанр
class GenreCreateAPIView(generics.CreateAPIView):
    """Енд поинт создания жанра
    """
    serializer_class = GenreSerializer
    queryset = Genre.objects.get_queryset()
    permission_classes = [permissions.IsAuthenticated & 
                          IsSuperUser | IsLibrarian]


class GenreUpdateAPIView(generics.UpdateAPIView):
    """Енд поинт обновления жанра
    """
    serializer_class = GenreSerializer
    queryset = Genre.objects.get_queryset()
    permission_classes = [permissions.IsAuthenticated & 
                          IsSuperUser | IsLibrarian]


class GenreDeleteAPIView(generics.DestroyAPIView):
    """Енд поинт удаления жанра
    """
    queryset = Genre.objects.get_queryset()
    permission_classes = [permissions.IsAuthenticated & 
                          IsSuperUser | IsLibrarian]


class GenreRetrieveAPIView(generics.RetrieveAPIView):
    """Енд поинт просмотра жанра
    """
    serializer_class = GenreSerializer
    queryset = Genre.objects.get_queryset()
    permission_classes = [permissions.AllowAny]


class GenreListAPIView(generics.ListAPIView):
    """Енд поинт списка жанров
    """
    serializer_class = GenreSerializer
    queryset = Genre.objects.get_queryset()
    permission_classes = [permissions.AllowAny]
