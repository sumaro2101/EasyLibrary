from django.contrib import admin

from library.models import (Author,
                            Order,
                            RequestExtension,
                            Book,
                            Publisher,
                            Volume,
                            Genre,
                            )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('book',
                    'tenant',
                    'count_extensions',
                    'time_order',
                    'time_return',
                    'status',
                    )


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name',
                    'last_name',
                    'surname',
                    'portrait',
                    )


@admin.register(RequestExtension)
class RequestExtensionAdmin(admin.ModelAdmin):
    list_display = ('order',
                    'applicant',
                    'time_request',
                    'receiving',
                    'time_response',
                    'solution',
                    )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
                  'publisher',
                  'name',
                  'image',
                  'best_seller',
                  'volume',
                  'quantity',
                  'num_of_volume',
                  'age_restriction',
                  'count_pages',
                  'year_published',
                  'circulation',
                  'is_published',
                  )


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'address',
                    'url',
                    'email',
                    'phone',
                    )


@admin.register(Volume)
class VolumeAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_ru',)
