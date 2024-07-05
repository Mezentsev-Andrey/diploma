from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from modules.models import Course, Lesson, Module, Subscription
from modules.paginations import CustomPagination
from modules.serializers import (
    CourseSerializer,
    LessonSerializer,
    ModuleSerializer,
    SubscriptionSerializer,
)
from users.permissions import IsModerator, IsOwner


class ModuleCreateAPIView(generics.CreateAPIView):
    """Контроллер для создания образовательного модуля"""

    serializer_class = ModuleSerializer
    permission_classes = [IsOwner | IsAdminUser]


class ModuleListAPIView(generics.ListAPIView):
    """Контроллер для вывода списка образовательных модулей"""

    serializer_class = ModuleSerializer
    queryset = Module.objects.all()
    pagination_class = CustomPagination
    permission_classes = [AllowAny]


class ModuleRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер для просмотра образовательного модуля"""

    serializer_class = ModuleSerializer
    queryset = Module.objects.all()
    permission_classes = [AllowAny]


class ModuleUpdateAPIView(generics.UpdateAPIView):
    """Контроллер для изменения образовательного модуля"""

    serializer_class = ModuleSerializer
    queryset = Module.objects.all()
    permission_classes = [IsOwner | IsAdminUser]


class ModuleDestroyAPIView(generics.DestroyAPIView):
    """Контроллер для удаления образовательного модуля"""

    queryset = Module.objects.all()
    permission_classes = [IsOwner | IsAdminUser]


class CourseListAPIView(generics.ListAPIView):
    """Контроллер для списка курсов."""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]


class CourseRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер для просмотра урока курса."""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner, IsAdminUser]


class CourseDetailAPIView(generics.RetrieveAPIView):
    """Контроллер для детального просмотра курса образовательного модуля."""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = IsAuthenticated


class CourseCreateAPIView(generics.CreateAPIView):
    """Контроллер для создания курса образовательного модуля."""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsModerator | IsOwner, IsAdminUser]


class CourseUpdateAPIView(generics.UpdateAPIView):
    """Контроллер для изменения курса образовательного модуля."""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsModerator | IsOwner, IsAdminUser]


class CourseDestroyAPIView(generics.DestroyAPIView):
    """Контроллер для удаления курса образовательного модуля."""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsModerator | IsOwner, IsAdminUser]


class LessonCreateAPIView(generics.CreateAPIView):
    """Контроллер для создания урока курса."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator | IsOwner, IsAdminUser]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(generics.ListAPIView):
    """Контроллер для вывода списка уроков курса."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination
    permission_classes = [AllowAny]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер для просмотра урока курса."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner, IsAdminUser]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Контроллер для изменения урока курса."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator | IsOwner, IsAdminUser]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Контроллер для удаления урока курса."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator | IsOwner, IsAdminUser]


class SubscriptionListAPIView(generics.ListAPIView):
    """Контроллер для вывода списка подписок."""

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    pagination_class = CustomPagination
    permission_classes = [AllowAny]


class SubscriptionCreateAPIView(generics.ListCreateAPIView):
    """Контроллер для создания подписки."""

    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsAdminUser]

    def get_queryset(self):
        # Возвращает подписки текущего пользователя
        return Subscription.objects.filter(subscriber=self.request.user)

    def perform_create(self, serializer):
        # Устанавливаем текущего пользователя как подписчика
        if serializer.validated_data[
            "subscription_type"
        ] == "module" and not serializer.validated_data.get("module"):
            raise ValidationError("Для подписки на модуль необходимо указать модуль.")
        if serializer.validated_data[
            "subscription_type"
        ] == "course" and not serializer.validated_data.get("course"):
            raise ValidationError("Для подписки на курс необходимо указать курс.")

        serializer.save(subscriber=self.request.user)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        module_id = self.request.data.get("module")

        # Получаем модуль
        module_item = get_object_or_404(Module, pk=module_id)

        # Инициализируем сообщение
        message = {}

        # Управление подпиской на модуль
        subs_module = Subscription.objects.filter(subscriber=user, module=module_item)

        if subs_module.exists():
            subs_module.delete()
            message["module"] = "Подписка на модуль удалена"
        else:
            Subscription.objects.create(subscriber=user, module=module_item)
            message["module"] = "Подписка на модуль добавлена"

        # Проверяем наличие связанного курса и управление подпиской на курс
        if getattr(module_item, "course", None):
            course_item = module_item.course

            subs_course = Subscription.objects.filter(
                subscriber=user, course=course_item
            )

            if subs_course.exists():
                subs_course.delete()
                message["course"] = "Подписка на курс удалена"
            else:
                Subscription.objects.create(subscriber=user, course=course_item)
                message["course"] = "Подписка на курс добавлена"

        # Возвращаем ответ в API
        return Response({"message": message})


class SubscriptionUpdateAPIView(generics.UpdateAPIView):
    """Контроллер для обновления подписки."""

    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsAdminUser]

    def get_queryset(self):
        # Возвращает подписки текущего пользователя
        return Subscription.objects.filter(subscriber=self.request.user)

    def perform_update(self, serializer):
        if serializer.validated_data[
            "subscription_type"
        ] == "module" and not serializer.validated_data.get("module"):
            raise ValidationError("Для подписки на модуль необходимо указать модуль.")
        if serializer.validated_data[
            "subscription_type"
        ] == "course" and not serializer.validated_data.get("course"):
            raise ValidationError("Для подписки на курс необходимо указать курс.")
        serializer.save()


class SubscriptionRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер для просмотра подписки."""

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsAdminUser]


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    """Контроллер для удаления подписки."""

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsAdminUser]
