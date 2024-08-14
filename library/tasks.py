from typing import Union

from library.services import send_mails
from library.models import Order, RequestExtension
from config.celery import app


@app.task()
def mail_task(order: Union[Order, RequestExtension],
              template: str) -> None:
    """Задача по отправке письма
    """
    return send_mails(order, template)
