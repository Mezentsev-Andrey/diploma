import typing

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from modules.models import Subscription


@shared_task
def send_updates(item: typing.Any) -> typing.Any:
    """Отправляет уведомления об обновлениях модуля на почту подписчикам."""

    active_subscriptions = Subscription.objects.filter(module=item)
    if active_subscriptions:
        for item in active_subscriptions:
            send_mail(
                subject=f"Обновление модуля: '{item.module.title}'",
                message=f"Информируем, что обновлен модуль: '{item.module.title}'\n"
                        f"\n* Данное сообщение является автоматическим уведомлением и не требует ответа.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[item.subscriber.email],
                fail_silently=False,
            )
