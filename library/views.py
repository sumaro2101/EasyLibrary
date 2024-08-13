from datetime import date, timedelta

from rest_framework import generics, status
from rest_framework import permissions
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from django_filters.rest_framework import backends as filters

from django.db.models import Q
from django.core.exceptions import (MultipleObjectsReturned,
                                    ObjectDoesNotExist,
                                    )
from django.conf import settings

from library.models import (Book,
                            Genre,
                            Author,
                            Publisher,
                            Volume,
                            Order,
                            RequestExtension,
                            )
from library.serializers import (BookCreateSerializer,
                                 BookRetrieveSerializer,
                                 GenreSerializer,
                                 AuthorSerializer,
                                 PublisherSerializer,
                                 VolumeSerializer,
                                 OrderOpenSerializer,
                                 OrderViewSerializer,
                                 OrderListViewSerializer,
                                 ExtensionAcceptSerializer,
                                 ExtensionCancelSerializer,
                                 ExtensionOpenSerializer,
                                 ExtensionRetrieveSerializer,
                                 ExtensionListSerializer,
                                 )
from library.permissions import IsLibrarian, IsSuperUser, IsCurrentUser
from library.task_manager import TaskManager
from library.paginators import (BasePaginate,
                                PaginageVolumes,
                                PaginagePublishers,
                                PaginageGenres,
                                PaginateExtensions
                                )


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
    filter_backends = (filters.DjangoFilterBackend,
                       OrderingFilter,)
    filterset_fields = ('name',
                        'publisher',
                        'best_seller',
                        'volume',
                        'age_restriction',
                        'year_published',
                        'is_published',
                        'author',
                        )
    ordering_fields = ('name',
                       'publisher',
                       'best_seller',
                       'age_restriction',
                       'year_published',
                       'is_published',
                       'circulation',
                       'quantity',
                       'count_pages',
                       'author',
                       )
    pagination_class = BasePaginate


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
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('last_name', 'first_name',)
    pagination_class = BasePaginate


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
    filter_backends = (filters.DjangoFilterBackend,
                       OrderingFilter,)
    filterset_fields = ('name', 'address',)
    ordering_fields = ('name',)
    pagination_class = PaginagePublishers


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
    filter_backends = (filters.DjangoFilterBackend,
                       OrderingFilter,)
    filterset_fields = ('name',)
    ordering_fields = ('name',)
    pagination_class = PaginageVolumes


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
    filter_backends = (OrderingFilter,)
    ordering_fields = ('name_en', 'name_ru',)
    pagination_class = PaginageGenres


# Выдача книг
class OrderOpenAPIView(generics.CreateAPIView):
    """Открытие выдачи книги
    """
    queryset = Order.objects.get_queryset()
    serializer_class = OrderOpenSerializer

    def create(self, request, *args, **kwargs):
        try:
            self.book = Book.objects.get(pk=self.kwargs['pk'])
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            return Response({'book': 'Данная книга не была найдена'},
                            status=status.HTTP_404_NOT_FOUND)
        age_restriction = self.book.age_restriction
        if age_restriction != 18:
            self.time_to_return_book = date.today() + timedelta(days=14)
        else:
            self.time_to_return_book = date.today() + timedelta(days=30)
        request.data['book'] = self.book
        request.data['tenant'] = self.request.user
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(book=self.book,
                        tenant=self.request.user,
                        time_return=self.time_to_return_book,
                        )


class OrderCloseAPIView(generics.DestroyAPIView):
    """Возврат выданной книги
    """
    queryset = Order.objects.get_queryset()
    permission_classes = [permissions.IsAuthenticated &
                          (IsLibrarian | IsSuperUser)]

    def perform_destroy(self, instance):
        instance.time_return = date.today()
        instance.status = 'end'
        instance.save(update_fields=('time_return', 'status'))
        task_manager = TaskManager(instance)
        task_manager.delete_periodic_task()
        TaskManager.launch_task(instance,
                                settings.TEMPLATES_TO_TASK['ORDER_CLOSE'],
                                )


class OrderRerieveAPIView(generics.RetrieveAPIView):
    """Просмотр статуса выданной книги
    """
    queryset = Order.objects.get_queryset().prefetch_related('book')
    serializer_class = OrderViewSerializer
    permission_classes = [permissions.IsAuthenticated &
                          (IsCurrentUser | IsLibrarian | IsSuperUser)]


class OrderListAPIView(generics.ListAPIView):
    """Просмотр списка выданных книг
    """
    queryset = Order.objects.get_queryset().prefetch_related('book')
    serializer_class = OrderListViewSerializer
    filter_backends = (filters.DjangoFilterBackend,
                       OrderingFilter,)
    filterset_fields = ('book', 'count_extensions',)
    ordering_fields = ('book',
                       'count_extensions',
                       'time_return',
                       )
    pagination_class = BasePaginate

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if not user.is_librarian and not user.is_superuser:
            queryset = queryset.filter(Q(tenant=self.request.user) &
                                       ~Q(status='end'))
        else:
            pass
        return queryset


class ExtensionOpenAPIView(generics.CreateAPIView):
    """Открытие запроса на продление
    """
    queryset = RequestExtension.objects.get_queryset()
    serializer_class = ExtensionOpenSerializer

    def create(self, request, *args, **kwargs):
        try:
            self.order = Order.objects.get(pk=self.kwargs['pk'])
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            return Response({'order': 'Выданной книги '
                             'не было найдено'
                             },
                            status=status.HTTP_404_NOT_FOUND)
        self.applicant = self.request.user
        request.data['order'] = self.order
        request.data['applicant'] = self.applicant
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(order=self.order,
                        applicant=self.applicant,
                        )


class ExtensionAcceptAPIView(generics.UpdateAPIView):
    """Принятие запроса на продление
    """
    queryset = RequestExtension.objects.get_queryset()
    serializer_class = ExtensionAcceptSerializer
    permission_classes = [permissions.IsAuthenticated &
                          (IsLibrarian | IsSuperUser)]


class ExtensionCancelAPIView(generics.UpdateAPIView):
    """Отказ запроса на продление
    """
    queryset = RequestExtension.objects.get_queryset()
    serializer_class = ExtensionCancelSerializer
    permission_classes = [permissions.IsAuthenticated &
                          (IsLibrarian | IsSuperUser)]


class ExtensionRetrieveAPIView(generics.RetrieveAPIView):
    """Просмотр запроса на продление
    """
    queryset = RequestExtension.objects.get_queryset().prefetch_related(
        'order__book',
    )
    serializer_class = ExtensionRetrieveSerializer
    permission_classes = [permissions.IsAuthenticated &
                          (IsCurrentUser | IsLibrarian | IsSuperUser)]


class ExtensionListAPIView(generics.ListAPIView):
    """Просмотр списка запросов
    """
    queryset = RequestExtension.objects.get_queryset().prefetch_related(
        'order__book',
    )
    serializer_class = ExtensionListSerializer
    filter_backends = (filters.DjangoFilterBackend,
                       OrderingFilter,)
    filterset_fields = ('order',
                        'applicant',
                        'solution',
                        )
    ordering_fields = ('solution',
                       'time_response',
                       'time_request',
                       )
    pagination_class = PaginateExtensions

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if not user.is_librarian and not user.is_superuser:
            queryset = queryset.filter(Q(applicant=self.request.user))
        else:
            pass
        return queryset
