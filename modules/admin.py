from django.contrib import admin

from modules.models import Lesson, Module, Subscription, Course


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
    )
    search_fields = ("title",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
    )
    search_fields = ("title",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "preview", "video")
    search_fields = ("title",)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("subscriber", "subscription_type")
    search_fields = ("subscriber",)
