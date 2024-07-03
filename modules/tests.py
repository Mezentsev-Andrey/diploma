from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from modules.models import Lesson, Module, Subscription
from users.models import User


class ModuleTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="test1@test.ru",
            is_superuser=True,
            is_staff=True,
        )
        self.module = Module.objects.create(
            name="Test Module", description="This is a test module"
        )
        self.client.force_authenticate(user=self.user)
        self.module = Module.objects.create(
            name="New module",
            description="New module description",
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_module_retrieve(self):
        """Тест на получение образовательного модуля"""

        url = reverse("modules:module_retrieve", args=(self.module.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.module.name)

    def test_module_create(self):
        """Тест создания образовательного модуля"""

        data = {"name": "New module", "description": "New module description"}
        url = reverse("modules:module_create")
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Module.objects.all().count(), 3)

    def test_module_list(self):
        """Тест на получение списка образовательных модулей"""

        url = reverse("modules:module_list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Module.objects.all().count(), 2)

    def test_module_update(self):
        """Тест изменения образовательного модуля"""

        url = reverse("modules:module_update", args=(self.module.pk,))
        new_data = {"description": "Test update module"}
        response = self.client.patch(url, data=new_data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("description"), "Test update module")

    def test_module_delete(self):
        """Тест удаления образовательного модуля"""

        url = reverse("modules:module_delete", args=(self.module.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Module.objects.all().count(), 1)


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="test2@test.ru",
            is_superuser=True,
            is_staff=True,
        )
        self.user.set_password("1234")
        self.client.force_authenticate(user=self.user)

        self.lesson = Lesson.objects.create(
            name="New lesson",
            description="New lesson description",
            video="youtube.com/watch/000",
            owner=self.user,
        )

    def test_lesson_retrieve(self):
        """Тест для просмотра урока"""

        response = self.client.get(
            reverse("modules:lesson_retrieve", args=(self.lesson.pk,))
        )
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson.name)

    def test_create_lesson(self):
        """Тест создания урока"""

        data = {"name": "New lesson", "description": "New lesson description"}
        url = reverse("modules:lesson_create")
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_list_lesson(self):
        """Тест получения списка уроков"""

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
                    "name": self.lesson.name,
                    "description": self.lesson.description,
                    "preview": None,
                    "video": "youtube.com/watch/000",
                    "module": None,
                    "owner": self.user.pk,
                },
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK),
        self.assertEqual(data, result)

    def test_update_lesson(self):
        """Тест обновления урока"""

        url = reverse("modules:lesson_update", args=(self.lesson.pk,))
        data = {
            "name": "Good lesson",
        }
        response = self.client.patch(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Good lesson")

    def test_delete_lesson(self):
        """Тест удаления урока"""

        url = reverse("modules:lesson_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test3@test.ru")
        self.user.set_password("12345")
        self.client.force_authenticate(user=self.user)
        self.module = Module.objects.create(name="test", owner=self.user)
        self.data = {

            "user": self.user.pk,
            "module": self.module.pk
    }

    def test_subscribe(self):
        """ Тест подписки к образовательному модулю """

        url = reverse("modules:create_subscription")
        response = self.client.post(url, self.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"message": "Подписка добавлена"})

    def test_unsubscribe(self):
        """ Тест отписки от образовательного модулю """

        url = reverse("modules:create_subscription")
        Subscription.objects.create(module=self.module, subscriber=self.user)
        response = self.client.post(url, self.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"message": "Подписка удалена"})
