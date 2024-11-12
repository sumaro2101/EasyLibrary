import json
from datetime import datetime, date

from typing import Union

from django_celery_beat.models import IntervalSchedule, PeriodicTask

from django.db.models import Q
from django.utils import timezone
from django.conf import settings

from django.core.exceptions import ObjectDoesNotExist

from library.models import Order, RequestExtension
from library.tasks import mail_task


class TaskManager:
    """Менеджер задач Celery
    Принимает в инициализацую модель Order
    """
    def __init__(self,
                 order: Order,
                 ) -> None:
        if not isinstance(order, Order):
            raise TypeError(f'{order}, не является моделью Order')
        self.order = order

    def _create_unique_name_to_task(self,
                                    model: Order,
                                    ) -> str:
        """Создание уникального имени для
        периодической задачи
        """
        app = model._meta.app_label
        name_model = model._meta.model_name
        pk = model.pk

        unique_name = f'{app}_{name_model}-OR_{pk}'
        return unique_name

    def _get_base_interval(self) -> IntervalSchedule:
        """Получение интервала
        Базовый интервал: every=1, period=DAYS
        """
        interval = IntervalSchedule.objects.filter(
            Q(every=1) &
            Q(period=IntervalSchedule.DAYS),
            )
        if not interval.exists():
            interval = IntervalSchedule.objects.create(
                every=1,
                period=IntervalSchedule.DAYS,
            )
        else:
            interval = interval.get()
        return interval

    def _handle_datetime_to_task(self,
                                 start_time: date,
                                 ) -> datetime:
        """Перерабатывает date в datatime время
        """
        year = start_time.year
        month = start_time.month
        day = start_time.day
        hour = settings.STANDART_HOUR_TO_TASK
        minute = settings.STANDART_MINUTE_TO_TASK

        date_to_task = datetime(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            tzinfo=timezone.get_current_timezone()
        )
        return date_to_task

    def _create_periodic_task(self,
                              model: Order,
                              ) -> PeriodicTask:
        """Создание периодической задачи
        """
        name = self._create_unique_name_to_task(model)
        time: date = model.time_return
        start_time = self._handle_datetime_to_task(time)
        interval = self._get_base_interval()
        kwargs = {
            'order': f'OR_{model.pk}',
            'template': settings.TEMPLATE_PERIODICK_TASK_PATH,
        }

        instance = PeriodicTask.objects.create(
            name=name,
            task='library.tasks.mail_task',
            interval=interval,
            start_time=start_time,
            kwargs=json.dumps(kwargs),
        )
        return instance

    def _update_periodic_task(self,
                              model: Order,
                              ) -> PeriodicTask:
        """Обновление периодической задачи
        """
        name = self._create_unique_name_to_task(model)
        pk = name.split('_')[-1]
        time: date = model.time_return
        start_time = self._handle_datetime_to_task(time)
        periodic_task = PeriodicTask.objects.filter(name=name)
        if periodic_task.exists():
            periodic_task = periodic_task.get()
            periodic_task.start_time = start_time
            periodic_task.save(update_fields=['start_time'])
        else:
            raise ObjectDoesNotExist(f'Задача по pk {pk} не найдена')

        return periodic_task

    def _delete_periodic_task(self,
                              model: Order,
                              ) -> None:
        """Удаление периодической задачи
        """
        name = self._create_unique_name_to_task(model)
        pk = name.split('_')[-1]
        periodic_task = PeriodicTask.objects.filter(name=name)
        if periodic_task.exists():
            periodic_task = periodic_task.get()
            periodic_task.start_time = None
            periodic_task.enabled = False
            periodic_task.save(update_fields=['start_time', 'enabled'])
        else:
            raise ObjectDoesNotExist(f'Задача по pk {pk} не найдена')

    def start_periodic_task(self) -> PeriodicTask:
        """Запуск периодической задачи
        """
        return self._create_periodic_task(self.order)

    def update_periodic_task(self) -> PeriodicTask:
        """Обновление периодической задачи
        """
        return self._update_periodic_task(self.order)

    def delete_periodic_task(self) -> None:
        """Удаление периодической задачи
        """
        return self._delete_periodic_task(self.order)

    @classmethod
    def launch_task(self,
                    model: Union[Order,
                                 RequestExtension,
                                 ],
                    template: str,
                    ) -> None:
        """Запуск мнгновенной задачи
        """
        model_name = model._meta.model_name
        if model_name == 'order':
            order = f'OR_{model.pk}'
        else:
            order = f'EX_{model.pk}'

        return mail_task.delay(order, template)
