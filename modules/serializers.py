from rest_framework import serializers

from modules.models import Lesson, Module, Subscription, Course
from modules.validators import ValidateURLResource


class ModuleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели образовательного модуля"""

    class Meta:
        model = Module
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [ValidateURLResource(field="video")]


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
