from datetime import timedelta, date

from rest_framework import serializers, validators

from django.db import transaction
from django.conf import settings

from library import models
from library.task_manager import TaskManager
from library.validators import (YearValidator,
                                PublishedValidator,
                                VolumeValidator,
                                OrderRepeatValidator,
                                BookQuantityValidator,
                                ExtensionValidator,
                                SomeUserValidator,
                                ResponseValidator,
                                CountExtensionsValidator,
                                IsActiveOrderValidator,
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
    count_books = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Author
        fields = ('pk',
                  'first_name',
                  'last_name',
                  'surname',
                  'portrait',
                  'books',
                  'count_books',
                  )
        validators = (validators.UniqueTogetherValidator(
            models.Author.objects.get_queryset(),
            ('first_name',
             'last_name',
             ),
        ),
                      )

    def get_count_books(self, obj):
        return obj.book_set.count()


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


class OrderOpenSerializer(serializers.ModelSerializer):
    """Сериализатор открытия выдачи книги
    """

    class Meta:
        model = models.Order
        fields = '__all__'
        read_only_fields = ('book',
                            'tenant',
                            'count_extensions',
                            'time_order',
                            'time_return',
                            'status',
                            )
        validators = (OrderRepeatValidator('book'),
                      BookQuantityValidator('book'),
                      )

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance = models.Order.objects.filter(
            pk=instance.pk,
            ).select_related(
                'book',
                'tenant',
            ).get()
        task_manager = TaskManager(instance)
        task_manager.start_periodic_task()
        task_manager.launch_task(instance,
                                 settings.TEMPLATES_TO_TASK['ORDER_OPEN'],
                                 )
        return instance


class OrderViewSerializer(serializers.ModelSerializer):
    """Сериализатор выданной книги
    """
    book = BookRetrieveSerializer(read_only=True)

    class Meta:
        model = models.Order
        fields = '__all__'


class OrderListViewSerializer(serializers.ModelSerializer):
    """Сериализатор списка выданных книг
    """
    book = serializers.StringRelatedField()

    class Meta:
        model = models.Order
        fields = ('book',
                  'time_order',
                  'time_return',
                  )


class ExtensionOpenSerializer(serializers.ModelSerializer):
    """Сериализатор открытия запроса на продление
    """

    class Meta:
        model = models.RequestExtension
        fields = '__all__'
        read_only_fields = ('order',
                            'applicant',
                            'time_request',
                            'receiving',
                            'time_response',
                            'solution',
                            )
        validators = (SomeUserValidator('order'),
                      IsActiveOrderValidator('order'),
                      ExtensionValidator('order'),
                      CountExtensionsValidator('order'),
                      )

    def create(self, validated_data):
        instance = super().create(validated_data)
        TaskManager.launch_task(instance,
                                settings.TEMPLATES_TO_TASK['EXTENSION_OPEN'],
                                )
        return instance


class ExtensionAcceptSerializer(serializers.ModelSerializer):
    """Сеарилизатор разрешения на продление
    """

    class Meta:
        model = models.RequestExtension
        fields = '__all__'
        read_only_fields = ('order',
                            'applicant',
                            'time_request',
                            'receiving',
                            'time_response',
                            'solution',
                            )
        validators = (ResponseValidator('solution'),)

    def update(self, instance, validated_data):
        with transaction.atomic():
            instance.receiving = self.context['request'].user
            instance.solution = 'accept'
            order = instance.order
            order.count_extensions += 1
            if order.book.age_restriction == 18:
                order.time_return = date.today() + timedelta(days=30)
            else:
                order.time_return = date.today() + timedelta(days=14)
            order.save(update_fields=('count_extensions',
                                      'time_return',
                                      ))
            extension = super().update(instance, validated_data)

        task_manager = TaskManager(order)
        task_manager.update_periodic_task()
        TaskManager.launch_task(extension,
                                settings.TEMPLATES_TO_TASK['EXTENSION_ACCEPT'],
                                )
        return extension


class ExtensionCancelSerializer(serializers.ModelSerializer):
    """Сеарилизатор отмены на продление
    """

    class Meta:
        model = models.RequestExtension
        fields = '__all__'
        read_only_fields = ('order',
                            'applicant',
                            'time_request',
                            'receiving',
                            'time_response',
                            'solution',
                            )
        validators = (ResponseValidator('solution'),)

    def update(self, instance, validated_data):
        instance.receiving = self.context['request'].user
        instance.solution = 'cancel'
        extension = super().update(instance, validated_data)
        TaskManager.launch_task(extension,
                                settings.TEMPLATES_TO_TASK['EXTENSION_CANCEL'],
                                )
        return extension


class ExtensionRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор просмотра запроса
    """
    order = OrderViewSerializer(read_only=True)

    class Meta:
        model = models.RequestExtension
        fields = '__all__'


class OrderField(serializers.ModelSerializer):
    """Поле для вывода заказа
    """
    book = serializers.StringRelatedField()

    class Meta:
        model = models.Order
        exclude = ('tenant',)


class LibrarianField(serializers.RelatedField):
    """Поле библеотекаря
    """
    def to_representation(self, value):
        if value:
            last_name = value.last_name if value.last_name else value.username
            first_name = value.first_name if value.first_name else ''
            return f'{last_name} {first_name} {value.email}'
        return None


class ExtensionListSerializer(serializers.ModelSerializer):
    """Сериализатор просмотра списка запросов
    """
    order = OrderField(read_only=True)
    receiving = LibrarianField(read_only=True)

    class Meta:
        model = models.RequestExtension
        exclude = ('applicant',)
