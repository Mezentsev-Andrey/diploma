from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    """Модель пользователя"""

    username = None
    email = models.EmailField(unique=True, verbose_name="Почта")
    avatar = models.ImageField(upload_to="users/", verbose_name="Аватар", **NULLABLE)
    phone_number = models.CharField(
        max_length=35, verbose_name="Номер телефона", **NULLABLE
    )
    city = models.CharField(max_length=150, verbose_name="Город", **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
