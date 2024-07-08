from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from modules.models import Course, Lesson, Module, Subscription
from modules.validators import ValidateURLResource


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [ValidateURLResource(field="video")]


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer(source="lesson_set", many=True, read_only=True)
    lessons_in_course_count = SerializerMethodField()
    is_subscribed = SerializerMethodField()
    subscribers = SubscriptionSerializer(
        source="course_for_subscription", many=True, read_only=True
    )

    def get_lessons_in_course_count(self, obj):
        return obj.lesson_set.all().count()

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        user = None
        if request:
            user = request.user
        return obj.course_for_subscription.filter(subscriber=user).exists()

    class Meta:
        model = Course
        fields = "__all__"


class ModuleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели образовательного модуля"""

    course = CourseSerializer(source="course_set", many=True, read_only=True)
    courses_in_module_count = SerializerMethodField()
    is_subscribed = SerializerMethodField()
    subscribers = SubscriptionSerializer(
        source="module_for_subscription", many=True, read_only=True
    )

    def get_courses_in_module_count(self, obj):
        return obj.course_set.all().count()

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        user = None
        if request:
            user = request.user
        return obj.module_for_subscription.filter(subscriber=user).exists()

    class Meta:
        model = Module
        fields = "__all__"
