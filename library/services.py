from datetime import date
from typing import Dict, Union
from django.urls import NoReverseMatch
from django.template import TemplateDoesNotExist, loader
from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from library.models import Order, RequestExtension


def get_info_order(model: Union[Order,
                                RequestExtension,
                                ]) -> Dict:
    """Отдает готовый словарь для контекста задачи
    """
    model_name = model._meta.model_name
    if model_name == 'order':
        extension = None
        model = model
    else:
        extension = model
        model = extension.order

    support = 'http://easyLibrary/support/ticket/'
    age_restriction = model.book.age_restriction
    if age_restriction == 18:
        count_days = 30
    else:
        count_days = 14
    if date.today() >= model.time_return:
        overdue_count = date.today() - model.time_return
        overdue_days = overdue_count.days
    else:
        overdue_days = None

    order_info = {
        'pk_extension': extension.pk if extension else None,
        'response_text': extension.response_text if extension else None,
        'pk_order': model.pk,
        'book_name': model.book.name,
        'age': f'{age_restriction}+',
        'count_days': count_days,
        'day_to_return': model.time_return,
        'support': support,
        'library': 'easyLibrary',
        'overdue_days': overdue_days if overdue_days else None,
    }
    return order_info


def send_mails(order: str,
               template: str) -> None:
    """Функция для оправки письма,
    является внутренней начинкой другой функции TASK

    Args:
    order (Model): Модель Order_pk
    template (str, None): Ссылка на html для отправки письма
    """
    model, pk = order.split('_')

    if model == 'OR':
        order = Order.objects.filter(pk=pk).select_related(
            'book',
            'tenant',
            )
        if order.exists():
            order = order.get()
            context = get_info_order(order)
            user_email = order.tenant.email
        else:
            raise ObjectDoesNotExist(
                f'Order по pk {order} не был найден',
            )

    elif model == 'EX':
        extension = RequestExtension.objects.filter(pk=pk).select_related(
            'order__book',
            'order__tenant',
        )
        if extension.exists():
            extension = extension.get()
            context = get_info_order(extension)
            user_email = extension.applicant.email
        else:
            raise ObjectDoesNotExist(
                f'Order по pk {order} не был найден',
            )

    email_template_name = template
    subject_template_name = settings.MAIL_SUBJECT_TASK_PATH
    server_mail: str = settings.EMAIL_HOST_USER
    user_email: str = (user_email,)

    try:
        subject = loader.render_to_string(
            subject_template_name,
            context=context,
            )
        subject = "".join(subject.splitlines())
    except TemplateDoesNotExist:
        raise TemplateDoesNotExist(
            f'По заданному пути: {subject_template_name} - '
            'шаблон не был найден',
            )
    except NoReverseMatch:
        raise NoReverseMatch('Ошибка при постоении пути')

    try:
        body = loader.render_to_string(email_template_name,
                                       context=context,
                                       )
    except TemplateDoesNotExist:
        raise TemplateDoesNotExist(
            f'По заданному пути: {email_template_name} - '
            'шаблон не был найден',
            )
    except NoReverseMatch:
        raise NoReverseMatch('Ошибка при постоении пути')

    email_message = EmailMultiAlternatives(subject,
                                           body,
                                           server_mail,
                                           user_email,
                                           )
    return email_message.send()
