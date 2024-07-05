from django.db import models

from config import settings

NULLABLE = {"blank": True, "null": True}


class Module(models.Model):
    """Модель образовательного модуля"""

    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name="Владелец",
    )
    price = models.PositiveIntegerField(default="10000", verbose_name="Цена модуля")

    def __str__(self):
        return f"{self.title} {self.owner}"

    class Meta:
        verbose_name = "Модуль"
        verbose_name_plural = "Модули"
        ordering = ("pk",)


class Course(models.Model):
    """Модель учебного курса"""

    module = models.ForeignKey(
        Module,
        related_name="module",
        on_delete=models.CASCADE,
        **NULLABLE,
        verbose_name="Модуль",
    )
    title = models.CharField(max_length=200, verbose_name="Название")
    preview = models.ImageField(
        upload_to="course_preview", verbose_name="Изображение", **NULLABLE
    )
    description = models.TextField(verbose_name="Описание")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name="Владелец",
    )
    price = models.PositiveIntegerField(default="5000", verbose_name="Цена курса")

    def __str__(self):
        return f"{self.title}, {self.module}, {self.price}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    """Модель урока"""

    course = models.ForeignKey(
        Course,
        related_name="course",
        on_delete=models.CASCADE,
        **NULLABLE,
        verbose_name="Курс",
    )
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    preview = models.ImageField(
        upload_to="lesson_preview", verbose_name="Изображение", **NULLABLE
    )
    video = models.CharField(max_length=300, verbose_name="Ссылка на видео", **NULLABLE)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name="Владелец",
    )

    def __str__(self):
        return f"{self.title}, {self.course}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Subscription(models.Model):
    """Модель подписки на образовательный модуль или курс"""

    SUBSCRIPTION_TYPE_CHOICES = [
        ("module", "Модуль"),
        ("course", "Курс"),
    ]

    subscriber = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Подписчик",
        **NULLABLE,
    )

    subscription_type = models.CharField(
        max_length=10,
        choices=SUBSCRIPTION_TYPE_CHOICES,
        default="course",
        verbose_name="Тип подписки",
    )

    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        verbose_name="Модуль",
        related_name="module_for_subscription",
        **NULLABLE,
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
        related_name="course_for_subscription",
        **NULLABLE,
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        if self.subscription_type == "module":
            return f"{self.subscriber} подписан на модуль {self.module}"
        elif self.subscription_type == "course":
            return f"{self.subscriber} подписан на курс {self.course}"
        else:
            return f"{self.subscriber} имеет подписку неизвестного типа"
