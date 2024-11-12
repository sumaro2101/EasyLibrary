# Title
Этот проект является API библиотекой и решает круг типичных задач любой библиотеки.
Какие задачи решает:
1. Облегчает поиск нужных книг
2. Увеличивает поток читателей
3. Улучшает популярность библиотеки
4. Уменьшает количество физических поситителей
5. Разгружает библиотекаря
6. Упрощает учет книг
7. Упрощает отслеживание выданных книг

# Utils
## Redis, Celery
В проекте используется Брокер сообщений Redis и воркер Celery
### Docker контейнер Redis
```yaml
redis:
    image: redis:7.2.5-alpine
    expose:
      - 6379
```

### Docker контейнер Celery Worker (Сокращенная версия)
```yaml
celery_worker:
    build: 
      context: .
      dockerfile: ./docker/django/Dockerfile
    image: config
    command: /start-celeryworker
    volumes:
      - .:/app
    env_file:
      - .env

celery_beat:
    build: 
      context: .
      dockerfile: ./docker/django/Dockerfile
    image: config
    command: /start-celerybeat
    volumes:
      - .:/app
    env_file:
      - .env
```

### Настройка Celery.
```python
# settings.py
INSTALLED_APPS = [
    'django_celery_beat',
]
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_BACKEND")
CELERY_RESULT_EXTENDED = True
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_BEAT_SCHEDULER = os.environ.get('DEFAULT_DATABASE_BEAT')
STANDART_HOUR_TO_TASK = 8
STANDART_MINUTE_TO_TASK = 0
```

### Инициализация Celery
```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

### TaskManager
```python
# Менеджер для работы Celery
# Создание переодической задачи
instance = <Order>
task_manager = TaskManager(instance)
task_manager.start_periodic_task()
```
```python
# Обновление переодической задачи
instance = <Order>
task_manager = TaskManager(instance)
task_manager.update_periodic_task()
```
```python
# Удаление переодической задачи
instance = <Order>
task_manager = TaskManager(instance)
task_manager.delete_periodic_task()
```
```python
# Запуск мнгновенной задачи
instance = <Order>
TaskManager.launch_task(
    instance,
    'path/to/html.html',
)
```

## Cachalot
Автоматизированный Кэш
### Настройка
```python
# settings.py
INSTALLED_APPS = [
    'cachalot',
]
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.environ.get('REDIS_CACHE'),
    }
}
```

### Использование
Использование данного функционала полностью автоматизированно.

## CorsHeaders
Проверка доступа к данном API извне посредством
инспекции Headers.
### Настройка
```python
# settings.py
INSTALLED_APPS = [
    'corsheaders',
]
CORS_ALLOWED_ORIGINS = ['http://localhost:8000']
CSRF_TRUSTED_ORIGINS = ['http://localhost:8000']
CORS_ALLOW_ALL_ORIGINS = False
```

### Использование
Использование данного функционала полностью автоматизированно.

## JsonWebToken
JWT токен позволяет производить аутентификацию и авторизацию
на очень высоком уровке безопасности.
### Настройка
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ]
}
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1)
}
```

### Энд поинты
```python
# urls.py
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)


urlpatterns = [
    path('api/token/',
          TokenObtainPairView.as_view(),
          name='token_obtain_pair',
          ),
     path('api/token/refresh/',
          TokenRefreshView.as_view(),
          name='token_refresh',
          ),
]
```

### Использование
Для аутентификации необходимо перейти на 
энд поинт по назначеному адрессу и ввести логин и пароль.
При правильных данных выводится JWT Bearer токен который необходимо
использовать для авторизации.

## OpenAI
Автогенерация документации на основе Энд поинтов,
моделей, сериализаторов.
Используется библиотека YASG.
### Настройка
```python
# settings.py
INSTALLED_APPS = [
    'drf_yasg',
]
SWAGGER_SETTINGS = {
    'VALIDATOR_URL': 'http://127.0.0.1:8000'
}
```

### Инициализация схемы
```python
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="EasyLibrary",
      default_version='v1',
      description="This documentation is say, how to use API servise",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="email@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
```

### Энд поинт
```python
urlpatterns = [
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
]
```

### Использование
Для получения документации по данному проекту
необходимо перейти на адресс:
http://localhost/redoc/
На данном адрессе вы найдете всю необходимую исчерпывающую
информацию о каждом элементе и объекте проекта.

# Validators
## Реализованны такие классы:
1. ValidatorSetPasswordUser
2. YearValidator
3. VolumeValidator
4. PublishedValidator
5. OrderRepeatValidator
6. BookQuantityValidator
7. ExtensionValidator
8. SomeUserValidator
9. ResponseValidator
10. CountExtensionsValidator
11. IsActiveOrderValidator

### ValidatorSetPasswordUser
```python
# Проверка корректности паролей
values = dict(password1='password', password2='password')
validator = ValidatorSetPasswordUser('password1', 'password2')
validator(values)
```

### YearValidator
```python
# Проверка корректности года публикации
# Если книга опубликована, год не может быть больше чем текущий.
value = dict(year_published=2020, is_published=True)
validator = YearValidator('year_published', 'is_published')
validator(value)
```

### VolumeValidator
```python
# Проверка корректности тома
# Если указан том, необходимо так же указать номер.
# Будет совершена проверка в рамках того что в данном томе
# еще не присутсвует данный номер.
volume = <Volume>
value = dict(volume=volume, num_of_volume=1)
validator = VolumeValidator('volume', 'num_of_volume')
validator(value)
```

### PublishedValidator
```python
# Проверка корректности данных исходя из статуса публикации.
# Если книга не опубликована она не может иметь тираж.
# Если книга не опубликована она не может быть лидером продаж.
value = dict(
    best_seller=True,
    circulation=10000,
    is_published=True,
    )
validator = PublishedValidator(
    'best_seller',
    'circulation',
    'is_published',
    )
validator(value)
```

### OrderRepeatValidator
```python
# Проверка выдачи книги.
# Если книга уже была выдана пользователю, то
# данный валидатор не даст снова ее выдать.
book = <Book>
value = dict(book=book)
validator = OrderRepeatValidator('book')
validator(value)
```

### BookQuantityValidator
```python
# Проверка количества книг.
# Если книг на складе больше нет, тогда выдать ее не получится.
book = <Book>
value = dict(book=book)
validator = BookQuantityValidator('book')
validator(value)
```

### ExtensionValidator
```python
# Контроль запросов на продление.
# Данный валидатор проверяет что запросов на продление
# еще нет, а так же если есть тогда они должны быть обработаны,
# в ином случае пользователю стоит подождать ответа на запрос.
order = <Order>
value = dict(order=order)
validator = ExtensionValidator('order')
validator(value)
```

### SomeUserValidator
```python
# Проверка пользователя.
# Пользователь может подавать запрос на продление
# только своего заказа книги.
order = <Order>
value = dict(order=order)
validator = SomeUserValidator('order')
validator(value)
```

### ResponseValidator
```python
# Проверка состояния запроса.
# Если по запросу был дан ответ, тогда выдать 
# повторно ответ уже не получится.
value = dict(solution='wait')
validator = ResponseValidator('solution')
validator(value)
```

### CountExtensionsValidator
```python
# Проверка количество продлений.
# Если количество продлений заказа
# уже на границе установленного уровня, тогда подать
# запрос больше не получится.
order = <Order>
value = dict(order=order)
validator = CountExtensionsValidator('order')
validator(value)
```

### IsActiveOrderValidator
```python
# Проверка статуса книги.
# Если книга уже была возвращена, тогда
# заявление больше подать не получится.
order = <Order>
value = dict(order=order)
validator = IsActiveOrderValidator('order')
validator(value)
```

# Other
## Регистрация пользователя
HandleCreateUser
```python
# Создание пользователя
# User - модель пользователя
user = HandleCreateUser(User,
                        validated_data,
                        )
user.create()
```

# How to use
## Для использования API нужно понимать, что есть 4 типа пользователей:
1. Администратор
2. Библиотекарь
3. Пользователь
4. Анонимный пользователь

## Описание:
1. Администратор может делать все и только он может создавать библиотекаря.
2. Библиотекарь может взаимодействовать так же со всей системой, но по опеределенным правилами.
3. Пользователь может только просматривать все таблицы, а так же брать книги если они есть в наличии и
создавать заявки на продление выданной книги.
4. Анонимный пользователь может только просматривать таблицы, не каких других действий он не может совершать.

## Администратор может:
1. Самое главное, Администратор может создавать библиотекаря и только он.
2. Все остальное.

## Библиотекарь может:
1. Cоздавать, просматривать, редактировать, удалять Книги.
2. Cоздавать, просматривать, редактировать, удалять Авторов.
3. Cоздавать, просматривать, редактировать, удалять Издателей.
4. Cоздавать, просматривать, редактировать, удалять Тома.
5. Cоздавать, просматривать, редактировать, удалять Жанры.
6. Открывать, просматривать, закрывать Выдачу книг.
7. Открывать, просматривать, принимать, отказывать заявки на Продление книг.

## Библиотекарь не может:
1. Создавать, редактировать, удалять любых пользователей включая себя.

## Пользователь может:
1. Открывать, просматривать, Выдачу книг.
2. Открывать, просматривать, заявку на Продление книг.
3. Создавать, просматривать, редактировать, удалять свой профиль.

## Пользователь не может:
1. Все остальное.

## Анонимный пользователь может:
1. Просматривать Книги, Авторов, Издателей, Жанры, Тома.

## Анонимный пользователь не может:
1. Все остальное.

# Rules
## Правила создания и обновления Книги:
1. Если книга опубликована - год ее написания не может быть больше ТЕКУЩЕГО.
2. Если книга не была опубликована - год ее написания может быть больше ТЕКУЩЕГО.
3. Если книга не была опубликована - она не может быть ЛИДЕРОМ продаж.
4. Если книга не была опубликована - она не может иметь ТИРАЖ.
5. Если у книги есть том - должен быть и номер присущей этой книги в ТОМЕ.
6. Поля обязательные: author, publisher, name, age_restriction, count_pages, year_published, genre, circulation.

## Правила создания и обновления Автора:
1. Поля имя и фамилия обязательны.
2. Поля имя и фамилия должны быть уникальной комбинацией.

## Правила создания и обновления Издателя:
1. Все поля обязательны.
2. Имя, телефон, Эмеил, URL, должны быть уникальны (то есть не повторяться).

## Правила создания и обновления Жанра:
1. Все поля обязательны.

## Правила создания и обновления Тома:
1. Все поля обязательны.

## Правила открытия выдачи книги:
1. Нельзя выдать одну и ту же книгу тому же пользователю,
если книга до сих пор не была возвращена.
2. Нельзя выдать книгу, если количество книг в библиотеке уже 0.

## Правила открытия заявления на продление выдачи книги:
1. Нельзя запросить продление, если заявление уже было подано и
оно до сих пор в статусе "wait" (то есть еще не было обработано библиотекарем).
2. Пользователь может открывать заявление только на свои книги которые были ему выданы.
3. Можно открывать заявления только на активную выдачу книги (то есть на ту которая еще не была возвращена).
4. Нельзя открывать заявление, если количество продлений уже 2 (можно продлевать только 2 раза).

## Правила обработки заявления на продления выдачи книги:
1. Одно заявление можно обработать только один раз, если статус заявление не 'wait' больше отвечать нельзя.


# Install
## Нужно заполнить файл .env всеми неоходимыми данными:
```python
DB_PASSWORD=password # Пароль Базы данных (использование).
POSTGRES_PASSWORD=password # Пароль Базы данных (настройка).
YANDEX_HOST_USER=host # Эмеил от имени которого будет рассылка.
YANDEX_PASSWORD_HOST=password # Пароль от Эмеила.
```

## Необходимо ввести команды:
Проект находится под контролем системы контеризации Docker.
```bash
docker-compose build
```
```bash
docker-compose up
```

# Tests

## Проведение тестов
Для проведения тестов вам нужно попасть внутрь основного контейнера
```bash
docker exec -it config bash
```
Если выходит ошибка попробуйте
```bash
docker exec -it config bin/bash
```
Затем запустить тесты
```bash
python manage.py test
```
У вас будет выполнено множество тестов.

# API URLS

## Книга
1. http://localhost/api/book/list/ GET - просмотр списка книг.
2. http://localhost/api/book/retrieve/"some_book_number"/ GET - просмотр книги.
3. http://localhost/api/book/create/ POST - создание книги.
4. http://localhost/api/book/update/"some_book_number"/ PATCH - обновление книги.
5. http://localhost/api/book/delete/"some_book_number"/ DELETE - удаление книги.

## Автор
1. http://localhost/api/author/list/ GET - просмотр списка авторов.
2. http://localhost/api/author/retrieve/"some_author_number"/ GET - просмотр автора.
3. http://localhost/api/author/create/ CREATE - создание автора.
4. http://localhost/api/author/update/"some_author_number"/ PATCH - обновление автора.
5. http://localhost/api/author/delete/"some_author_number"/ DELETE - удаление автора.

## Издатель
1. http://localhost/api/publisher/list/ GET - просмотр списка издателей.
2. http://localhost/api/publisher/retrieve/"some_publisher_number"/ GET - просмотр автора.
3. http://localhost/api/publisher/create/ CREATE - создание издателя.
4. http://localhost/api/publisher/update/"some_publisher_number"/ PATCH - обновление автора.
5. http://localhost/api/publisher/delete/"some_publisher_number"/ DELETE - удаление автора.

## Том
1. http://localhost/api/volume/list/ GET - просмотр списка томов.
2. http://localhost/api/volume/retrieve/"some_volume_number"/ GET - просмотр тома.
3. http://localhost/api/volume/create/ CREATE - создание тома.
4. http://localhost/api/volume/update/"some_volume_number"/ PATCH - обновление тома.
5. http://localhost/api/volume/delete/"some_volume_number"/ DELETE - удаление тома.

## Жанр
1. http://localhost/api/genre/list/ GET - просмотр списка жанров.
2. http://localhost/api/genre/retrieve/"some_genre_number"/ GET - просмотр жанра.
3. http://localhost/api/genre/create/ CREATE - создание жанра.
4. http://localhost/api/genre/update/"some_genre_number"/ PATCH - обновление жанра.
5. http://localhost/api/genre/delete/"some_genre_number"/ DELETE - удаление жанра.

## Выдача книг
1. http://localhost/api/order/open/"some_book_number"/ CREATE - открытие выдачи книги.
2. http://localhost/api/order/close/"some_order_number"/ DELETE - закрытие выдачи книги.
3. http://localhost/api/order/retrieve/"some_order_number"/ GET - просмотр выдачи.
4. http://localhost/api/order/list/ GET - просмотр списка выдач.

## Запрос на продление выдачи
1. http://localhost/api/extension/open/"some_order_number"/ CREATE - открытие заявление на продление.
2. http://localhost/api/extension/accept/"some_extension_number"/ PATCH - принятие продления.
3. http://localhost/api/extension/cancel/"some_extension_number"/ PATCH - отказ от продления.
4. http://localhost/api/extension/retrieve/"some_extension_number"/ GET - просмотр заявления.
5. http://localhost/api/extension/list/ GET - просмотра списка заявлений.


# Info
Проект состоит из ~2800 строк кода не считая тестов.

Тестов 101 штука.
Тестов написанно ~2500 строк кода.


# Future Plans

В дальнейшей работе есть цель улучшить оптимизацию.

Улучшения связанные с программой могут быть:
1. Добавление таблицы "Редакция".
2. Добавление таблицы "Должники" для санкций и штрафов.
3. Внедрение посторонего API для оплаты штрафов например: Stripe.
4. Логика связанная с снятием санкий по сигналу оплаты.
5. Онлайн книги.
6. Аудио книги.
