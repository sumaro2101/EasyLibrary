from django.db import models
from django.urls import reverse

from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class Book(models.Model):
    """Модель книги
    """
    author = models.ManyToManyField("library.Author",
                                    verbose_name='авторы',
                                    help_text='Авторы данной книги',
                                    )

    publisher = models.ForeignKey("library.Publisher",
                                  verbose_name='издатель',
                                  help_text='Издательство данной книги',
                                  on_delete=models.CASCADE,
                                  )

    name = models.CharField(max_length=300,
                            verbose_name='название',
                            help_text='Название книги',
                            )

    image = models.ImageField(upload_to=f'book/{name}/',
                              null=True,
                              blank=True,
                              verbose_name='изображение',
                              help_text='Изображение книги',
                              )

    best_seller = models.BooleanField(default=False,
                                      verbose_name='лидер продаж',
                                      help_text='Является ли книга\
                                        лидером продаж',
                                        )

    volume = models.BooleanField(default=False,
                                 verbose_name='том',
                                 help_text='Является ли книга частью тома',
                                 )

    num_of_volume = models.PositiveSmallIntegerField(null=True,
                                                     blank=True,
                                                     verbose_name='номер из тома',
                                                     help_text='Какая по номеру книга в томе',
                                                     )

    age_restriction = models.PositiveSmallIntegerField(
        choices=[
            (0, '0+'),
            (6, '6+'),
            (12, '12+'),
            (16, '16+'),
            (18, '18+'),
            ],
        verbose_name='возрастные ограничения',
        help_text='Возрастные ограничения для данной книги',
        )

    count_pages = models.PositiveIntegerField(
        verbose_name='количество страниц',
        help_text='Количество страниц данной книги',
        )

    year_published = models.DateField()

    genre = models.ManyToManyField("library.Genre",
                                   verbose_name='жанры',
                                   help_text='Жанры данной книги',
                                   )

    circulation = models.PositiveIntegerField(verbose_name='тираж',
                                              help_text='Тираж данной книги',
                                              )

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

    def __str__(self):
        return f'{self.name} {self.age_restriction}+'

    def get_absolute_url(self):
        return reverse("book_detail", kwargs={"pk": self.pk})


class Author(models.Model):
    """Модель Автора книг
    """
    first_name = models.CharField(max_length=150,
                                  verbose_name='имя автора',
                                  help_text='Имя указанного автора книги',
                                  )

    last_name = models.CharField(max_length=150,
                                 verbose_name='фамилия автора',
                                 help_text='Фамилия указанного автора',
                                 )

    surname = models.CharField(max_length=150,
                                   verbose_name='отчество',
                                   help_text='Отчество указанного автора',
                                   blank=True,
                                   null=True,
                                   )

    portrait = models.ImageField(upload_to=f'author/{first_name}/{last_name}/',
                                 blank=True,
                                 null=True,
                                 verbose_name='портрет',
                                 help_text='Портрет автора',
                                 )

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    def get_absolute_url(self):
        return reverse("author_detail", kwargs={"pk": self.pk})


class Publisher(models.Model):
    """Модель издателя
    """
    name = models.CharField(max_length=200,
                            verbose_name='имя издателя',
                            unique=True,
                            help_text='Имя издателя',
                            )

    adress = models.CharField(max_length=300,
                              verbose_name='адресс издателя',
                              help_text='Адресс издателя',
                              )

    url = models.URLField(max_length=256,
                          verbose_name='сайт',
                          help_text='Сайт издателя',
                          unique=True,
                          )

    email = models.EmailField(max_length=254,
                              verbose_name='эмеил',
                              help_text='Эмеил издателя',
                              unique=True,
                              )

    phone = PhoneNumberField(verbose_name='номер телефона',
                             help_text='Контактный номер\
                             телефона издательства',
                             unique=True,
                             )

    class Meta:
        verbose_name = "издатель"
        verbose_name_plural = "издатели"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("publisher_detail", kwargs={"pk": self.pk})


class Genre(models.Model):
    """Модель жанра
    """
    name_en = models.CharField(max_length=200,
                               verbose_name='имя англ',
                               help_text='Жанр на английском',
                               unique=True,
                               )

    name_ru = models.CharField(max_length=200,
                               verbose_name='имя ру',
                               help_text='Жанр на русском',
                               unique=True,
                               )

    class Meta:
        verbose_name = "жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name_ru

    def get_absolute_url(self):
        return reverse("genre_detail", kwargs={"pk": self.pk})