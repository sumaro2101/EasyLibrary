from typing import Union

from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from library.services import send_mails
from library.models import Order, RequestExtension
from config.celery import app


@app.task()
def mail_task(order: Union[Order, RequestExtension],
              template: str) -> None:
    """Задача по отправке письма
    """
    return send_mails(order, template)

@app.task()
def test_mail():
    subject = 'subject'
    body = 'test',
    server_mail = 'suguhapa@yandex.ru'
    user_email = 'yukiu217@gmail.com'
    email_message = EmailMultiAlternatives(subject,
                                           body,
                                           server_mail,
                                           user_email,
                                           )
    email_message.send()