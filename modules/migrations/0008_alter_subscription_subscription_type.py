# Generated by Django 4.2.9 on 2024-07-08 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("modules", "0007_alter_subscription_subscription_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subscription",
            name="subscription_type",
            field=models.CharField(
                choices=[("module", "Модуль"), ("course", "Курс")],
                default="module",
                max_length=10,
                verbose_name="Тип подписки",
            ),
        ),
    ]
