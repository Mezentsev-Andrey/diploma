# Generated by Django 4.2.9 on 2024-07-03 12:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200, verbose_name="Название")),
                (
                    "preview",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="course_preview",
                        verbose_name="Изображение",
                    ),
                ),
                ("description", models.TextField(verbose_name="Описание")),
                (
                    "price",
                    models.PositiveIntegerField(
                        default="5000", verbose_name="Цена курса"
                    ),
                ),
            ],
            options={
                "verbose_name": "Курс",
                "verbose_name_plural": "Курсы",
            },
        ),
        migrations.CreateModel(
            name="Lesson",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="Название")),
                ("description", models.TextField(verbose_name="Описание")),
                (
                    "preview",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="lesson_preview",
                        verbose_name="Изображение",
                    ),
                ),
                (
                    "video",
                    models.CharField(
                        blank=True,
                        max_length=300,
                        null=True,
                        verbose_name="Ссылка на видео",
                    ),
                ),
            ],
            options={
                "verbose_name": "Урок",
                "verbose_name_plural": "Уроки",
            },
        ),
        migrations.CreateModel(
            name="Module",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200, verbose_name="Название")),
                ("description", models.TextField(verbose_name="Описание")),
                (
                    "price",
                    models.PositiveIntegerField(
                        default="10000", verbose_name="Цена модуля"
                    ),
                ),
            ],
            options={
                "verbose_name": "Модуль",
                "verbose_name_plural": "Модули",
                "ordering": ("pk",),
            },
        ),
        migrations.CreateModel(
            name="Subscription",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "subscription_type",
                    models.CharField(
                        choices=[("module", "Модуль"), ("course", "Курс")],
                        default="module",
                        max_length=10,
                        verbose_name="Тип подписки",
                    ),
                ),
                (
                    "course",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="course_for_subscription",
                        to="modules.course",
                        verbose_name="Курс",
                    ),
                ),
                (
                    "module",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="module_for_subscription",
                        to="modules.module",
                        verbose_name="Модуль",
                    ),
                ),
            ],
            options={
                "verbose_name": "Подписка",
                "verbose_name_plural": "Подписки",
            },
        ),
    ]
