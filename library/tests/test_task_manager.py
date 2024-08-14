from datetime import date, timedelta, datetime

from django_celery_beat.models import IntervalSchedule, PeriodicTask

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from library.models import Author, Book, Genre, Order, Publisher, Volume
from library.task_manager import TaskManager


class TestTaskManager(TestCase):
    """Тесты менеджера задач
    """
    def setUp(self) -> None:
        user = get_user_model().objects.create(
            username='user',
            email='user@gmail.com',
            phone='+7 (900) 900 2000',
            password='testpassword',
            is_librarian=True,
            is_staff=True,
        )
        author = Author.objects.create(first_name='author',
                                       last_name='author_last',
                                       surname='surname',
                                       )
        publisher = Publisher.objects.create(
            name='publisher',
            address='new-york',
            url='https://www.publisher.com/',
            email='publisher@gmail.com',
            phone='+79136001000',
        )
        volume = Volume.objects.create(
            name='fantasy_volume',
        )
        genre = Genre.objects.create(
            name_en='fantasy',
            name_ru='Фэнтези',
        )
        book = Book.objects.create(
            publisher=publisher,
            name='book',
            best_seller=True,
            volume=volume,
            num_of_volume=1,
            age_restriction=16,
            count_pages=300,
            year_published=2015,
            circulation=1203,
            is_published=True,
        )
        book.author.add(author)
        book.genre.add(genre)
        self.order = Order.objects.create(
            book=book,
            tenant=user,
            time_return=date.today() + timedelta(days=30),
        )

    def test_raise_init_task_manager(self):
        """Тест ошибки при инициализации
        """
        book = self.order.book

        with self.assertRaises(TypeError):
            TaskManager(book)

    def test_create_task_name(self):
        """Тест создания имени задачи
        """
        task_manager = TaskManager(self.order)
        name = task_manager._create_unique_name_to_task(self.order)

        self.assertEqual(name, f'library_order-OR_{self.order.pk}')

    def test_create_base_interval(self):
        """Тест создания интервала при первом
        использовании
        """
        task_manager = TaskManager(self.order)
        interval = task_manager._get_base_interval()

        self.assertEqual(interval.every, 1)
        self.assertEqual(interval.period, 'days')
        self.assertEqual(IntervalSchedule.objects.count(), 1)

    def test_get_base_interval(self):
        """Тест получения интервала
        """
        task_manager = TaskManager(self.order)
        # Создание
        interval1 = task_manager._get_base_interval()
        # Получение
        interval2 = task_manager._get_base_interval()

        self.assertEqual(interval1, interval2)
        self.assertEqual(IntervalSchedule.objects.count(), 1)

    def test_handle_time_to_task(self):
        """Тест переработчика времени
        """
        task_manager = TaskManager(self.order)

        time = task_manager._handle_datetime_to_task(
            self.order.time_return,
            )
        time_return = self.order.time_return
        time_to_check = datetime(
            year=time_return.year,
            month=time_return.month,
            day=time_return.day,
            hour=8,
            minute=0,
            tzinfo=timezone.get_current_timezone()
        )
        self.assertEqual(time, time_to_check)

    def test_create_task(self):
        """Тест создания задачи
        """
        task_manager = TaskManager(self.order)
        instance = task_manager.start_periodic_task()
        time_return = self.order.time_return
        time_to_check = datetime(
            year=time_return.year,
            month=time_return.month,
            day=time_return.day,
            hour=8,
            minute=0,
            tzinfo=timezone.get_current_timezone()
        )

        self.assertEqual(PeriodicTask.objects.count(), 1)
        self.assertEqual(instance, PeriodicTask.objects.get())
        self.assertEqual(instance.start_time, time_to_check)

    def test_update_task(self):
        """Тест обновления задачи
        """
        task_manager = TaskManager(self.order)
        task_manager.start_periodic_task()
        self.order.time_return = date.today() + timedelta(days=60)
        self.order.save(update_fields=['time_return'])
        instance = task_manager.update_periodic_task()
        time_return = date.today() + timedelta(days=60)
        time_to_check = datetime(
            year=time_return.year,
            month=time_return.month,
            day=time_return.day,
            hour=8,
            minute=0,
            tzinfo=timezone.get_current_timezone()
        )

        self.assertEqual(instance.start_time, time_to_check)

    def test_delete_task(self):
        """Тест удаления задачи
        """
        task_manager = TaskManager(self.order)
        task_manager.start_periodic_task()
        task_manager.delete_periodic_task()
        name_task = task_manager._create_unique_name_to_task(self.order)
        instance = PeriodicTask.objects.get(name=name_task)

        self.assertIsNone(instance.start_time)
        self.assertFalse(instance.enabled)
