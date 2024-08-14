from django.db import models
from django.urls import reverse

from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


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
        return reverse("library:author_retrieve", kwargs={"pk": self.pk})


class Publisher(models.Model):
    """Модель издателя
    """
    name = models.CharField(max_length=200,
                            verbose_name='имя издателя',
                            unique=True,
                            help_text='Имя издателя',
                            )

    address = models.CharField(max_length=300,
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
        return reverse("library:publisher_retrieve", kwargs={"pk": self.pk})


class Volume(models.Model):
    """Модель тома
    """
    name = models.CharField(max_length=150,
                            help_text='Имя тома',
                            verbose_name='имя тома',
                            )

    class Meta:
        verbose_name = 'Том'
        verbose_name_plural = 'Тома'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("library:volume_retrieve", kwargs={"pk": self.pk})


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
        return reverse("library:genre_retrieve", kwargs={"pk": self.pk})


class Book(models.Model):
    """Модель книги
    """
    author = models.ManyToManyField(Author,
                                    verbose_name='авторы',
                                    help_text='Авторы данной книги',
                                    )

    publisher = models.ForeignKey(Publisher,
                                  verbose_name='издатель',
                                  help_text='Издательство данной книги',
                                  on_delete=models.CASCADE,
                                  )

    name = models.CharField(max_length=300,
                            verbose_name='название',
                            help_text='Название книги',
                            )

    quantity = models.PositiveIntegerField(
        verbose_name='количество',
        help_text='Количество книг в библиотеке',
        default=1,
        )

    image = models.ImageField(upload_to=f'book/{name}/',
                              null=True,
                              blank=True,
                              verbose_name='изображение',
                              help_text='Изображение книги',
                              )

    best_seller = models.BooleanField(verbose_name='лидер продаж',
                                      default=False,
                                      help_text='Является ли книга '
                                      'лидером продаж',
                                      )

    volume = models.ForeignKey(Volume,
                               verbose_name='том',
                               help_text='Том книги',
                               related_name='books',
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True,
                               )

    num_of_volume = models.PositiveSmallIntegerField(
        null=True,
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

    year_published = models.PositiveIntegerField(
        verbose_name='дата издательства',
        help_text='Дата издательства книги',
        )

    genre = models.ManyToManyField(Genre,
                                   verbose_name='жанры',
                                   help_text='Жанры данной книги',
                                   )

    circulation = models.PositiveIntegerField(verbose_name='тираж',
                                              help_text='Тираж данной книги',
                                              )

    is_published = models.BooleanField(verbose_name='публикация',
                                       help_text='Опублинована ли книга',
                                       default=True,
                                       )

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ['name']

    def __str__(self):
        return f'{self.name} {self.age_restriction}+'

    def get_absolute_url(self):
        return reverse("library:book_retrieve", kwargs={"pk": self.pk})


class Order(models.Model):
    """Модель выдачи книг
    """
    book = models.ForeignKey(Book,
                             verbose_name='книга',
                             on_delete=models.CASCADE,
                             help_text='Книга которую выдали',
                             )

    tenant = models.ForeignKey("users.User",
                               verbose_name='пользователь',
                               on_delete=models.SET_NULL,
                               help_text='На кого была выдана книга',
                               null=True,
                               )

    count_extensions = models.SmallIntegerField(verbose_name='продления',
                                                help_text='Количество '
                                                'продлений которые '
                                                'уже были сделаны',
                                                default=0,
                                                )

    time_order = models.DateField(auto_now_add=True,
                                  verbose_name='время выдачи',
                                  help_text='Время когда книга была выдана',
                                  )

    time_return = models.DateField(verbose_name='время возврата',
                                   help_text='Время когда нужно '
                                   'вернуть книгу',
                                   )

    status = models.CharField(choices=[('active', 'активно'),
                                       ('end', 'закончено'),
                                       ],
                              default='active',
                              max_length=30,
                              )

    class Meta:
        verbose_name = 'выдача'
        verbose_name_plural = 'выдачи'
        ordering = ['time_order']

    def __str__(self):
        return f'{self.time_order} - {self.status}'

    def get_absolute_url(self):
        return reverse("order_retrieve", kwargs={"pk": self.pk})


class RequestExtension(models.Model):
    """Модель запроса на продление
    """
    order = models.ForeignKey(Order,
                              verbose_name='выдача',
                              on_delete=models.CASCADE,
                              help_text='Объект выдачи книги',
                              )

    applicant = models.ForeignKey("users.User",
                                  verbose_name='заявщик',
                                  on_delete=models.SET_NULL,
                                  related_name='extensions',
                                  help_text='Заявщик который хочет продлить',
                                  default=None,
                                  blank=True,
                                  null=True,
                                  )

    time_request = models.DateTimeField(auto_now_add=True,
                                        verbose_name='время запроса',
                                        help_text='Время запроса',
                                        )

    receiving = models.ForeignKey("users.User",
                                  verbose_name='принимающий',
                                  help_text='Библиотекарь который '
                                  'обработал запрос',
                                  on_delete=models.SET_DEFAULT,
                                  default=None,
                                  null=True,
                                  blank=True,
                                  )

    time_response = models.DateTimeField(auto_now=True,
                                         verbose_name='время ответа',
                                         help_text='Время ответа',
                                         )

    response_text = models.TextField(verbose_name='ответ',
                                     help_text='Письменный ответ от '
                                     'библиотекаря',
                                     null=True,
                                     blank=True,
                                     )

    solution = models.CharField(choices=[('accept', 'принят'),
                                         ('cancel', 'отменен'),
                                         ('wait', 'ожидание'),
                                         ],
                                verbose_name='решение',
                                help_text='Принятое решение библиотекарем',
                                default='wait',
                                max_length=30,
                                )

    class Meta:
        verbose_name = 'запрос'
        verbose_name_plural = 'запросы'
        ordering = ['time_request']

    def __str__(self):
        return f'{self.time_request} - {self.solution}'

    def get_absolute_url(self):
        return reverse("extension_retrieve", kwargs={"pk": self.pk})
