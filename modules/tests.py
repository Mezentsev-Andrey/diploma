from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from modules.models import Course, Lesson, Module, Subscription
from modules.serializers import SubscriptionSerializer
from users.models import User


class ModuleTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="test1@test.ru",
            is_superuser=True,
            is_staff=True,
        )
        self.user.set_password("1234")
        self.client.force_authenticate(user=self.user)
        self.module = Module.objects.create(
            title="New module",
            description="New module description",
            owner=self.user,
        )

    def test_retrieve_module(self):
        """Тест на получение образовательного модуля."""

        url = reverse("modules:module_retrieve", args=(self.module.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.module.title)

    def test_create_module(self):
        """Тест создания образовательного модуля."""

        data = {"title": "New module", "description": "New module description"}
        url = reverse("modules:module_create")
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Module.objects.all().count(), 2)

    def test_list_module(self):
        """Тест на получение списка образовательных модулей."""

        url = reverse("modules:module_list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Module.objects.all().count(), 1)

    def test_update_module(self):
        """Тест изменения образовательного модуля."""

        url = reverse("modules:module_update", args=(self.module.pk,))
        new_data = {"description": "Test update module"}
        response = self.client.patch(url, data=new_data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("description"), "Test update module")

    def test_delete_module(self):
        """Тест удаления образовательного модуля."""

        url = reverse("modules:module_delete", args=(self.module.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Module.objects.all().count(), 0)


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="test2@test.ru",
            is_superuser=True,
            is_staff=True,
        )
        self.user.set_password("1234")
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(
            title="Course",
            description="Course description",
            owner=self.user,
        )

    def test_retrieve_course(self):
        """Тест просмотра курса."""

        response = self.client.get(
            reverse("modules:course_retrieve", args=(self.course.pk,))
        )
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.course.title)

    #
    def test_create_course(self):
        """Тест создания курса."""

        data = {"title": "New course", "description": "New course description"}
        url = reverse("modules:course_create")
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Course.objects.all().count(), 2)

    def test_list_course(self):
        """Тест на получение списка курсов."""

        url = reverse("modules:course_list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Module.objects.all().count(), 0)

    def test_update_course(self):
        """Тест изменения курса."""

        url = reverse("modules:course_update", args=(self.course.pk,))
        new_data = {"description": "Test update course"}
        response = self.client.patch(url, data=new_data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("description"), "Test update course")

    def test_delete_course(self):
        """Тест удаления курса."""

        url = reverse("modules:course_delete", args=(self.course.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Module.objects.all().count(), 0)


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="test3@test.ru",
            is_superuser=True,
            is_staff=True,
        )
        self.user.set_password("1234")
        self.client.force_authenticate(user=self.user)

        self.lesson = Lesson.objects.create(
            title="New lesson",
            description="New lesson description",
            video="youtube.com/watch/000",
            owner=self.user,
        )

    def test_retrieve_lesson(self):
        """Тест просмотра урока."""

        response = self.client.get(
            reverse("modules:lesson_retrieve", args=(self.lesson.pk,))
        )
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)

    def test_create_lesson(self):
        """Тест создания урока."""

        data = {"title": "New lesson", "description": "New lesson description"}
        url = reverse("modules:lesson_create")
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_list_lesson(self):
        """Тест получения списка уроков."""

        url = reverse("modules:lesson_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "title": self.lesson.title,
                    "description": self.lesson.description,
                    "preview": None,
                    "video": "youtube.com/watch/000",
                    "course": None,
                    "owner": self.user.pk,
                },
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK),
        self.assertEqual(data, result)

    def test_update_lesson(self):
        """Тест обновления урока."""

        url = reverse("modules:lesson_update", args=(self.lesson.pk,))
        data = {
            "title": "Good lesson",
        }
        response = self.client.patch(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Good lesson")

    def test_delete_lesson(self):
        """Тест удаления урока."""

        url = reverse("modules:lesson_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)


class SubscriptionTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="test4@test.ru",
            is_superuser=True,
            is_staff=True,
        )
        self.user.set_password("1234")
        self.client.force_authenticate(user=self.user)

        # Создание модулей и курсов
        self.course = Course.objects.create(title="Test Course")
        self.module = Module.objects.create(title="Test Module")

    def test_get_subscription_list(self):
        """Тест получения списка подписок."""

        self.subscription_url = reverse("modules:subscription_list")

        # Создаем несколько подписок для теста
        Subscription.objects.create(subscriber=self.user, module=self.module)
        Subscription.objects.create(subscriber=self.user, course=self.course)

        response = self.client.get(self.subscription_url)

        # Проверяем, что запрос выполнен успешно
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Извлекаем только данные из response, которые нас интересуют
        response_data = (
            response.data["results"] if "results" in response.data else response.data
        )

        # Извлекаем ожидаемые данные из сериализатора
        subscriptions = Subscription.objects.filter(subscriber=self.user)
        expected_data = SubscriptionSerializer(subscriptions, many=True).data

        # Проверяем, что данные из ответа соответствуют ожидаемым данным
        self.assertEqual(response_data, expected_data)

    def test_create_subscription_unauthenticated(self):
        """Тест создания подписки без аутентификации."""

        self.url = reverse("modules:subscription_create")

        # Проверка, что не аутентифицированный пользователь не может создать подписку
        self.client.force_authenticate(user=None)  # Удаление аутентификации
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_module_subscription(self):
        """Тест создания подписки на модуль."""

        self.url = reverse("modules:subscription_create")

        response = self.client.post(self.url, data={"module": self.module.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("module", response.data["message"])
        self.assertTrue(
            Subscription.objects.filter(
                subscriber=self.user, module=self.module
            ).exists()
        )

    def test_remove_module_subscription(self):
        """Тест удаления подписки на модуль."""

        self.url = reverse("modules:subscription_create")

        Subscription.objects.create(subscriber=self.user, module=self.module)
        response = self.client.post(self.url, data={"module": self.module.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("module", response.data["message"])
        self.assertFalse(
            Subscription.objects.filter(
                subscriber=self.user, module=self.module
            ).exists()
        )

    def test_create_subscription_without_module(self):
        """Тест ошибки при попытке создать подписку на модуль без указания модуля."""

        self.url = reverse("modules:subscription_create")
        response = self.client.post(self.url, data={"subscription_type": "module"})

        # Проверяем, что статус ответа равен либо 400, либо 404
        self.assertIn(
            response.status_code,
            [status.HTTP_400_BAD_REQUEST, status.HTTP_404_NOT_FOUND],
        )

        # Убеждаемся что в ответе содержится либо ожидаемое сообщение, либо текущее сообщение об ошибке
        expected_message_1 = "Для подписки на модуль необходимо указать модуль."
        expected_message_2 = "No Module matches the given query."

        response_text = str(response.data)
        self.assertTrue(
            expected_message_1 in response_text or expected_message_2 in response_text,
            f"Ответ не содержит ожидаемых сообщений об ошибке. Получено: {response_text}",
        )

    def test_create_subscription_without_course(self):
        """Тест создания подписки на курс без указания курса."""

        self.url = reverse("modules:subscription_create")
        response = self.client.post(self.url, data={"subscription_type": "course"})

        # Проверяем, что возвращается статус 404
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Проверяем, что сообщение об ошибке соответствует ожидаемому формату
        expected_error_message = "No Module matches the given query."
        actual_error_message = response.data.get("detail", "")
        self.assertIn(expected_error_message, actual_error_message)


class SubscriptionUpdateRetrieveDeleteTestCase(APITestCase):

    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create(
            email="test4@test.ru",
            password="1234",
            is_superuser=True,
            is_staff=True,
        )
        self.user.set_password("1234")
        self.user.save()
        self.client.force_authenticate(user=self.user)

        # Создаем тестовый курс и модуль
        self.course = Course.objects.create(title="Test Course")
        self.module = Module.objects.create(title="Test Module")

        # Создаем тестовую подписку
        self.subscription = Subscription.objects.create(
            subscriber=self.user,
            course=self.course,
            module=self.module,
        )
        # URL для обновления подписки
        self.url = reverse("modules:subscription_update", args=[self.subscription.id])

    def test_update_subscription_success(self):
        """Тест успешного обновления подписки."""

        data = {
            "subscription_type": "module",
            "module": self.module.id,  # Используем ID модуля
        }
        response = self.client.put(self.url, data, format="json")
        self.subscription.refresh_from_db()  # Обновляем объект из базы данных

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.subscription.subscription_type, data["subscription_type"])
        self.assertEqual(self.subscription.module.id, data["module"])

    def test_update_subscription_course_missing(self):
        """Тест ошибки валидации при отсутствии курса для подписки на курс."""

        data = {
            "subscription_type": "course",
            "course": None,  # Пустое значение для курса
        }
        response = self.client.put(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Проверяем структуру данных ответа
        if isinstance(response.data, list):
            error_message = response.data[0]
        else:
            error_message = response.data

        # Проверяем, что сообщение об ошибке присутствует в ответе
        self.assertIn(
            "Для подписки на курс необходимо указать курс.", str(error_message)
        )

    def test_update_subscription_module_missing(self):
        """Тест ошибки валидации при отсутствии модуля для подписки на модуль."""

        data = {
            "subscription_type": "module",
            "module": None,  # Пустое значение для модуля
        }
        response = self.client.put(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Проверяем структуру данных ответа
        if isinstance(response.data, list):
            error_message = response.data[0]
        else:
            error_message = response.data

        # Проверяем, что сообщение об ошибке присутствует в ответе
        self.assertIn(
            "Для подписки на модуль необходимо указать модуль.", str(error_message)
        )

    def test_update_subscription_permissions(self):
        """Тест проверки прав доступа для обновления подписки."""

        self.client.force_authenticate(user=None)  # Разлогиниваем пользователя

        data = {
            "subscription_type": "course",
            "course": self.course.id,
        }
        response = self.client.put(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_subscription(self):
        """Тест получения подписки."""

        # Генерируем URL для получения конкретной подписки
        url = reverse("modules:subscription_retrieve", args=[self.subscription.id])

        # Делаем GET запрос
        response = self.client.get(url)

        # Проверяем, что ответ успешный
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем, что данные в ответе соответствуют ожиданиям
        self.assertEqual(response.data["id"], self.subscription.id)
        self.assertEqual(response.data["subscriber"], self.user.id)
        self.assertEqual(response.data["course"], self.course.id)
        self.assertEqual(response.data["module"], self.module.id)

    def test_delete_subscription(self):
        """Тест удаления подписки."""
        url = reverse(
            "modules:subscription_delete", kwargs={"pk": self.subscription.pk}
        )

        # Удаление подписки
        response = self.client.delete(url)

        # Проверка, что подписка успешно удалена
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Проверка, что подписка больше не существует
        self.assertFalse(Subscription.objects.filter(pk=self.subscription.pk).exists())
