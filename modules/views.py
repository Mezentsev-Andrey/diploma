from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from modules.models import Lesson, Module, Subscription, Course
from modules.paginations import CustomPagination
from modules.serializers import (LessonSerializer, ModuleSerializer,
                                 SubscriptionSerializer, CourseSerializer)
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
    permission_classes = [IsAuthenticated]


class ModuleRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер для просмотра образовательного модуля"""

    serializer_class = ModuleSerializer
    queryset = Module.objects.all()


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
    """ Контроллер для списка курсов."""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер для просмотра урока курса."""

    queryset = Course.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModerator | IsOwner)


class CourseDetailAPIView(generics.RetrieveAPIView):
    """ Контроллер для детального просмотра курса образовательного модуля."""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = IsAuthenticated


class CourseCreateAPIView(generics.CreateAPIView):
    """Контроллер для создания курса образовательного модуля."""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (~IsModerator, IsAuthenticated)


class CourseUpdateAPIView(generics.UpdateAPIView):
    """Контроллер для изменения курса образовательного модуля."""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    # permission_classes = (IsAuthenticated, IsModerator | IsOwner)


class CourseDestroyAPIView(generics.DestroyAPIView):
    """Контроллер для удаления курса образовательного модуля."""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    # permission_classes = (IsOwner | ~IsModerator)


class LessonCreateAPIView(generics.CreateAPIView):
    """Контроллер для создания урока курса."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModerator, IsOwner)

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(generics.ListAPIView):
    """Контроллер для вывода списка уроков курса."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер для просмотра урока курса."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModerator | IsOwner)


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Контроллер для изменения урока курса."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsModerator | IsOwner)


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Контроллер для удаления урока курса."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsOwner | ~IsModerator)


class SubscriptionListCreateView(generics.ListCreateAPIView):
    """Контроллер для создания подписок и их списков."""
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Возвращает подписки текущего пользователя
        return Subscription.objects.filter(subscriber=self.request.user)

    def perform_create(self, serializer):
        # Устанавливаем текущего пользователя как подписчика
        if serializer.validated_data['subscription_type'] == 'module' and not serializer.validated_data.get('module'):
            raise ValidationError("Для подписки на модуль необходимо указать модуль.")
        if serializer.validated_data['subscription_type'] == 'course' and not serializer.validated_data.get('course'):
            raise ValidationError("Для подписки на курс необходимо указать курс.")

        serializer.save(subscriber=self.request.user)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        module_id = self.request.data.get("module")

        # Получаем модуль
        module_item = get_object_or_404(Module, pk=module_id)

        # Получаем все курсы, связанные с этим модулем
        related_courses = Course.objects.filter(modules=module_item)

        # Проверяем наличие подписок на модуль
        subs_module = Subscription.objects.filter(subscriber=user, module=module_item)

        # Проверяем наличие подписок на все курсы, связанные с этим модулем
        subs_courses = Subscription.objects.filter(subscriber=user, course__in=related_courses)

        # Инициализируем сообщения
        message = {}

        # Управление подпиской на модуль
        if subs_module.exists():
            subs_module.delete()
            message["module"] = "Подписка на модуль удалена"
        else:
            Subscription.objects.create(subscriber=user, module=module_item)
            message["module"] = "Подписка на модуль добавлена"

        # Управление подписками на курсы
        if subs_courses.exists():
            subs_courses.delete()
            message["course"] = "Подписки на связанные курсы удалены"
        else:
            for course in related_courses:
                Subscription.objects.create(subscriber=user, course=course)
            message["course"] = "Подписки на связанные курсы добавлены"

        # Возвращаем ответ в API
        return Response({"message": message})


class SubscriptionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """    Контроллер  для просмотра, обновления и удаления подписки."""
    serializer_class = SubscriptionSerializer
    permission_classes = IsAuthenticated

    def get_queryset(self):
        # Возвращает подписки текущего пользователя
        return Subscription.objects.filter(subscriber=self.request.user)

    def perform_update(self, serializer):
        if serializer.validated_data['subscription_type'] == 'module' and not serializer.validated_data.get('module'):
            raise ValidationError("Для подписки на модуль необходимо указать модуль.")
        if serializer.validated_data['subscription_type'] == 'course' and not serializer.validated_data.get('course'):
            raise ValidationError("Для подписки на курс необходимо указать курс.")
        serializer.save()
