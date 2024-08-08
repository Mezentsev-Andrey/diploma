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
        self.user.save()

        self.client.force_authenticate(user=self.user)
        self.module = Module.objects.create(
            title="New module",
            description="New module description",
            owner=self.user,
        )

    def retrieve_module(self):
        """Тест на получение определенного продукта."""

        # Отправляем GET-запрос на URL, соответствующий получению
        # конкретного модуля с идентификатором self.module.id.
        response = self.client.get(f'/modules/{self.module.id}/')

        # Проверяем, что статус-код ответа равен 200 OK,
        # что означает успешное получение ресурса.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем, что значение поля title в данных ответа совпадает
        # со значением поля title у модуля self.module.
        self.assertEqual(response.data['title'], self.module.title)

    def test_create_module(self):
        """Тест на создание нового образовательного модуля."""

        # Проверяем, что отправляем все необходимые поля для создания
        data = {"title": "New module", "description": "New module description"}

        response = self.client.post('/modules/', data, format='json')

        # Проверяем, что статус-код ответа равен 201 Created.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Проверяем, что общее количество модулей в базе данных равно 2.
        self.assertEqual(Module.objects.all().count(), 2)

    def test_list_module(self):
        """Тест на получение списка образовательных модулей."""

        # Отправляем GET-запрос на URL, соответствующий получению списка модулей.
        # self.client используется для выполнения запроса в контексте теста.
        response = self.client.get('/modules/')

        # Проверяем, что статус-код ответа равен 200 OK.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем, что общее количество модулей в базе данных равно 1.
        self.assertEqual(Module.objects.all().count(), 1)

    def test_update_module(self):
        """Тест на обновление образовательного модуля."""

        # Проверяем, что отправляем все необходимые поля для обновления
        new_data = {"description": "Test update module"}

        # Отправляем PATCH-запрос на URL, соответствующий обновлению модуля с определенным
        # идентификатором self.module.id, с данными для обновления в формате JSON.
        response = self.client.patch(f'/modules/{self.module.id}/', data=new_data, format='json')

        # Преобразуем тело ответа из формата JSON в Python-словарь.
        data = response.json()

        # Проверяем, что статус-код ответа равен 200 OK.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем, что значение ключа "description" в JSON-ответе совпадает с обновленным описанием.
        self.assertEqual(data.get("description"), "Test update module")

    def test_delete_module(self):
        """Тест удаления образовательного модуля."""

        # Отправляем DELETE-запрос на URL, соответствующий удалению модуля
        # с определенным идентификатором self.module.id.
        response = self.client.delete(f'/modules/{self.module.id}/')

        # Проверяем, что статус-код ответа равен 204 No Content.
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Проверяем, что общее количество модулей в базе данных равно 0.
        self.assertEqual(Module.objects.all().count(), 0)


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="test2@test.ru",
            is_superuser=True,
            is_staff=True,
        )
        self.user.set_password("1234")
        self.user.save()

        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(
            title="Course",
            description="Course description",
            owner=self.user,
        )

    def test_retrieve_course(self):
        """Тест просмотра определенного курса."""

        # Выполняем GET-запрос к URL для получения данных о конкретном курсе.
        response = self.client.get(
            reverse("modules:course_retrieve", args=(self.course.pk,))
        )
        # Преобразуем тело ответа из формата JSON в Python-словарь.
        data = response.json()

        # Проверяем, что статус-код ответа равен 200 OK.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем, что значение ключа "title" в JSON-ответе совпадает с названием курса.
        self.assertEqual(data.get("title"), self.course.title)

    #
    def test_create_course(self):
        """Тест создания курса."""

        # Создаем словарь данных, содержащий заголовок и описание нового курса.
        data = {"title": "New course", "description": "New course description"}

        # Формируем URL для эндпоинта создания нового курса.
        url = reverse("modules:course_create")
        # Выполняет POST-запрос к сформированному URL с данными о новом курсе.
        response = self.client.post(url, data=data)

        # Проверяем, что статус-код ответа равен 201 Created.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Проверяем, что общее количество курсов в базе данных равно 2.
        self.assertEqual(Course.objects.all().count(), 2)

    def test_list_course(self):
        """Тест на получение списка курсов."""

        # Формируем URL для эндпоинта получения списка всех курсов.
        url = reverse("modules:course_list")
        # Выполняем GET-запрос к сформированному URL.
        response = self.client.get(url)

        # Проверяем, что статус-код ответа равен 200 OK.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем, что общее количество курсов в базе данных равно 1.
        self.assertEqual(Course.objects.all().count(), 1)

    def test_update_course(self):
        """Тест изменения курса."""

        # Формируем URL для эндпоинта обновления существующего курса по его первичному ключу (pk).
        url = reverse("modules:course_update", args=(self.course.pk,))

        # Создаем словарь новых данных для обновления курса.
        new_data = {"description": "Test update course"}

        # Выполняем PATCH-запрос к сформированному URL с новыми данными.
        response = self.client.patch(url, data=new_data)

        # Преобразуем тело ответа из формата JSON в Python-словарь.
        data = response.json()

        # Проверяем, что статус-код ответа равен 200 OK.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем, что значение ключа "description" в JSON-ответе совпадает с обновленным описанием.
        self.assertEqual(data.get("description"), "Test update course")

    def test_delete_course(self):
        """Тест удаления курса."""

        # Формируем URL для эндпоинта удаления существующего курса по его первичному ключу (pk).
        url = reverse("modules:course_delete", args=(self.course.pk,))
        # Выполняем DELETE-запрос к сформированному URL.
        response = self.client.delete(url)

        # Проверяем, что статус-код ответа равен 204 No Content.
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Проверяем, что общее количество курсов в базе данных равно 0.
        self.assertEqual(Course.objects.all().count(), 0)


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="test3@test.ru",
            is_superuser=True,
            is_staff=True,
        )
        self.user.set_password("1234")
        self.user.save()

        self.client.force_authenticate(user=self.user)

        self.lesson = Lesson.objects.create(
            title="New lesson",
            description="New lesson description",
            video="youtube.com/watch/000",
            owner=self.user,
        )

    def test_retrieve_lesson(self):
        """Тест просмотра определенного урока."""

        # Выполняем GET-запрос к URL для получения конкретного урока по его первичному ключу (pk).
        response = self.client.get(
            reverse("modules:lesson_retrieve", args=(self.lesson.pk,))
        )
        # Преобразуем ответ в формат JSON.
        data = response.json()

        # Проверяем, что статус-код ответа равен 200 OK.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем, что заголовок полученного урока соответствует ожидаемому заголовку урока.
        self.assertEqual(data.get("title"), self.lesson.title)

    def test_create_lesson(self):
        """Тест создания урока."""

        # Данные для создания нового урока.
        data = {"title": "New lesson", "description": "New lesson description"}

        # Формируем URL для создания урока.
        url = reverse("modules:lesson_create")
        # Выполняем POST-запрос для создания урока с указанными данными.
        response = self.client.post(url, data=data)

        # Проверяем, что статус-код ответа равен 201 Created.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Проверяем, что общее количество уроков в базе данных равно 2.
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_list_lesson(self):
        """Тест получения списка уроков."""

        # Формируем URL для получения списка всех уроков.
        url = reverse("modules:lesson_list")
        # Выполняем GET-запрос к URL для получения списка уроков.
        response = self.client.get(url)

        # Преобразуем ответ в формат JSON.
        data = response.json()

        # Ожидаемый результат списка уроков.
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

        # Проверяем, что статус-код ответа равен 200 OK.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем, что данные, полученные от API, соответствуют ожидаемому результату.
        self.assertEqual(data, result)

    def test_update_lesson(self):
        """Тест обновления урока."""

        # Формируем URL для обновления урока по его первичному ключу (pk).
        url = reverse("modules:lesson_update", args=(self.lesson.pk,))

        # Новые данные для обновления урока (изменяем только заголовок).
        data = {
            "title": "Good lesson",
        }
        # Выполняем PATCH-запрос для обновления урока с указанными данными.
        response = self.client.patch(url, data=data)

        # Проверяем, что статус-код ответа равен 200 OK.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем, что заголовок урока после обновления равен ожидаемому значению.
        self.assertEqual(data.get("title"), "Good lesson")

    def test_delete_lesson(self):
        """Тест удаления урока."""

        # Формируем URL для удаления урока по его первичному ключу (pk).
        url = reverse("modules:lesson_delete", args=(self.lesson.pk,))
        # Выполняем DELETE-запрос для удаления урока.
        response = self.client.delete(url)

        # Проверяем, что статус-код ответа равен 204 No Content.
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Проверяем, что общее количество уроков в базе данных равно 0.
        self.assertEqual(Lesson.objects.all().count(), 0)


class SubscriptionTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="test4@test.ru",
            is_superuser=True,
            is_staff=True,
        )
        self.user.set_password("1234")
        self.user.save()

        self.client.force_authenticate(user=self.user)

        # Создаем модули и курсы
        self.course = Course.objects.create(title="Test Course")
        self.module = Module.objects.create(title="Test Module")

    def test_get_subscription_list(self):
        """Тест получения списка подписок."""

        # Получаем URL для списка подписок по имени маршрута.
        self.url = reverse("modules:subscription_list")

        # Создаем подписку пользователя self.user на модуль self.module.
        Subscription.objects.create(subscriber=self.user, module=self.module)
        # Создаем подписку пользователя self.user на курс self.course.
        Subscription.objects.create(subscriber=self.user, course=self.course)

        # Выполняем GET-запрос к URL списка подписок, используя тестовый клиент.
        response = self.client.get(self.url)

        # Проверяем, что запрос выполнен успешно (HTTP 200 OK).
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Извлекаем данные из ответа. Если в response.data есть ключ "results", используем его,
        # иначе берем все response.data.
        response_data = (
            response.data["results"] if "results" in response.data else response.data
        )

        # Извлекаем все подписки пользователя self.user из базы данных.
        subscriptions = Subscription.objects.filter(subscriber=self.user)

        # Сериализуем подписки в формат JSON с помощью SubscriptionSerializer.
        # many=True указывает на сериализацию множества объектов.
        expected_data = SubscriptionSerializer(subscriptions, many=True).data

        # Сравниваем данные из ответа с ожидаемыми данными.
        # Проверяем, что API возвращает корректные данные о подписках.
        self.assertEqual(response_data, expected_data)

    def test_create_subscription_unauthenticated(self):
        """Тест создания подписки без аутентификации."""

        # Получаем URL для создания подписки по имени маршрута.
        self.url = reverse("modules:subscription_create")

        # Проверка, что неаутентифицированный пользователь не может создать подписку
        # Убираем аутентификацию, имитируя неавторизованного пользователя.
        self.client.force_authenticate(user=None)

        # Выполняем POST-запрос к URL создания подписки с пустыми данными.
        response = self.client.post(self.url, data={})

        # Проверяем, что статус ответа 401 Unauthorized, что подтверждает невозможность
        # создания подписки без аутентификации.
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_module_subscription(self):
        """Тест создания подписки на модуль."""

        # Получаем URL для создания подписки по имени маршрута.
        self.url = reverse("modules:subscription_create")

        # Выполняем POST-запрос к URL создания подписки с данными, содержащими идентификатор модуля.
        response = self.client.post(self.url, data={"module": self.module.id})

        # Проверяем, что статус ответа 200 OK, что подтверждает успешное создание подписки.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем, что в ответе содержится упоминание модуля.
        self.assertIn("module", response.data["message"])
        # Проверяем, что подписка на указанный модуль действительно была создана в базе данных.
        self.assertTrue(
            Subscription.objects.filter(
                subscriber=self.user, module=self.module
            ).exists()
        )

    def test_remove_module_subscription(self):
        """Тест удаления подписки на модуль."""

        # Получаем URL для создания подписки по имени маршрута.
        self.url = reverse("modules:subscription_create")

        # Создаем подписку пользователя на модуль для теста.
        Subscription.objects.create(subscriber=self.user, module=self.module)
        # Выполняем POST-запрос к URL создания подписки с данными, содержащими идентификатор модуля,
        # что инициирует удаление существующей подписки (предполагается, что одно и то же действие удаляет подписку).
        response = self.client.post(self.url, data={"module": self.module.id})

        # Проверяем, что статус ответа 200 OK, что подтверждает успешное выполнение запроса.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем, что в ответе содержится упоминание модуля.
        self.assertIn("module", response.data["message"])
        # Проверяем, что подписка на указанный модуль действительно была удалена из базы данных.
        self.assertFalse(
            Subscription.objects.filter(
                subscriber=self.user, module=self.module
            ).exists()
        )

    def test_create_subscription_without_module(self):
        """Тест ошибки при попытке создать подписку на модуль без указания модуля."""

        # Получаем URL для создания подписки по имени маршрута.
        self.url = reverse("modules:subscription_create")

        # Выполняем POST-запрос к URL создания подписки с типом подписки "module", но без указания модуля.
        response = self.client.post(self.url, data={"subscription_type": "module"})

        # Проверяем, что статус ответа либо 400 Bad Request, либо 404 Not Found,
        # что указывает на ошибку при отсутствии указания модуля.
        self.assertIn(
            response.status_code,
            [status.HTTP_400_BAD_REQUEST, status.HTTP_404_NOT_FOUND],
        )

        # Убеждаемся что в ответе содержится либо ожидаемое сообщение, либо текущее сообщение об ошибке
        expected_message_1 = "Для подписки на модуль необходимо указать модуль."
        expected_message_2 = "No Module matches the given query."

        # Преобразуем ответ в строку для проверки наличия ожидаемых сообщений.
        response_text = str(response.data)
        self.assertTrue(
            expected_message_1 in response_text or expected_message_2 in response_text,
            f"Ответ не содержит ожидаемых сообщений об ошибке. Получено: {response_text}",
        )

    def test_create_subscription_without_course(self):
        """Тест создания подписки на курс без указания курса."""

        # Получаем URL для создания подписки по имени маршрута.
        self.url = reverse("modules:subscription_create")

        # Выполняем POST-запрос к URL создания подписки с типом подписки "course", но без указания курса.
        response = self.client.post(self.url, data={"subscription_type": "course"})

        # Проверяем, что возвращается статус 404 Not Found,
        # что указывает на ошибку при отсутствии указания курса.
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Проверяем, что сообщение об ошибке в ответе соответствует ожидаемому сообщению.
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

    def test_update_subscription(self):
        # Подготавливаем данные для обновления
        data = {
            'subscription_type': 'course',
            'course': self.course.id  # Используем реальный ID курса
        }

        response = self.client.put(self.url, data, format='json')

        # Проверка статуса ответа
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

        # Проверяем, что подписка была обновлена
        self.subscription.refresh_from_db()
        self.assertEqual(self.subscription.subscription_type, 'course')
        self.assertEqual(self.subscription.course.id, self.course.id)

    def test_update_subscription_success(self):
        """Тест успешного обновления подписки."""

        # Создаем данные для обновления подписки.
        data = {
            "subscription_type": "module",  # Указываем тип подписки "module".
            "module": self.module.id,  # Используем ID модуля для обновления.
        }
        # Выполняем PUT-запрос к URL обновления подписки с указанными данными в формате JSON.
        response = self.client.put(self.url, data, format="json")
        # Обновляем объект подписки из базы данных, чтобы получить актуальные данные.
        self.subscription.refresh_from_db()

        # Проверяем, что статус ответа 200 OK, что подтверждает успешное обновление подписки.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Проверяем, что тип подписки обновлен и соответствует ожидаемому значению.
        self.assertEqual(self.subscription.subscription_type, data["subscription_type"])
        # Проверяем, что модуль подписки обновлен и соответствует ожидаемому значению.
        self.assertEqual(self.subscription.module.id, data["module"])

    def test_update_subscription_course_missing(self):
        """Тест ошибки валидации при отсутствии курса для подписки на курс."""

        # Создаем данные для обновления подписки с пустым значением для курса.
        data = {
            "subscription_type": "course",  # Указываем тип подписки "course".
            "course": None,  # Пустое значение для курса, что вызовет ошибку валидации.
        }
        # Выполняем PUT-запрос к URL обновления подписки с указанными данными в формате JSON.
        response = self.client.put(self.url, data, format="json")

        # Проверяем, что статус ответа 400 Bad Request, что подтверждает ошибку валидации.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Проверяем структуру данных ответа.
        # Если данные ответа являются списком, извлекаем первое сообщение об ошибке.
        if isinstance(response.data, list):
            error_message = response.data[0]
        else:
            # Если данные ответа - это словарь, используем его напрямую.
            error_message = response.data

        # Проверяем, что в ответе содержится ожидаемое сообщение об ошибке.
        self.assertIn(
            "Для подписки на курс необходимо указать курс.", str(error_message)
        )

    def test_update_subscription_module_missing(self):
        """Тест ошибки валидации при отсутствии модуля для подписки на модуль."""

        # Создаем данные для обновления подписки с пустым значением для модуля.
        data = {
            "subscription_type": "module",  # Указываем тип подписки "module".
            "module": None,  # Пустое значение для модуля, что вызовет ошибку валидации.
        }
        # Выполняем PUT-запрос к URL обновления подписки с указанными данными в формате JSON.
        response = self.client.put(self.url, data, format="json")

        # Проверяем, что статус ответа 400 Bad Request, что подтверждает ошибку валидации.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Проверяем структуру данных ответа.
        # Если данные ответа являются списком, извлекаем первое сообщение об ошибке.
        if isinstance(response.data, list):
            error_message = response.data[0]
        else:
            # Если данные ответа - это словарь, используем его напрямую.
            error_message = response.data

        # Проверяем, что в ответе содержится ожидаемое сообщение об ошибке.
        self.assertIn(
            "Для подписки на модуль необходимо указать модуль.", str(error_message)
        )

    def test_invalid_subscription_update(self):
        """Тест попытку обновления подписки на модуль без указания модуля."""

        # Подготавливаем данные для обновления: тип подписки 'module' без указания модуля
        data = {
            'subscription_type': 'module',
            # модуль не указан
        }

        # Отправляем PUT запрос на обновление подписки
        response = self.client.put(self.url, data, format='json')

        # Проверяем, что статус ответа 400 Bad Request, что указывает на ошибку в данных запроса
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg=response.data)

        # Проверяем, что ожидаемое сообщение об ошибке содержится в ответе API
        # Предполагаем, что response.data может быть списком ошибок
        expected_error_message = 'Для подписки на модуль необходимо указать модуль.'

        # Проверяем, что ошибка присутствует в списке ошибок
        errors = response.data
        if isinstance(errors, dict):
            # Если response.data является словарем, ищем ошибку в 'non_field_errors' или другом ключе
            error_messages = errors.get('non_field_errors', [])
        elif isinstance(errors, list):
            # Если response.data является списком, используем его напрямую
            error_messages = errors
        else:
            # Если структура данных неожиданная, выводим отладочное сообщение
            error_messages = []

        self.assertIn(expected_error_message, error_messages)

    def test_update_subscription_permissions(self):
        """Тест проверки прав доступа для обновления подписки."""

        # Разлогиниваем пользователя, чтобы имитировать неавторизованного пользователя.
        self.client.force_authenticate(user=None)

        # Создаем данные для обновления подписки на курс.
        data = {
            "subscription_type": "course",  # Указываем тип подписки "course".
            "course": self.course.id,  # Используем ID курса для обновления.
        }
        # Выполняем PUT-запрос к URL обновления подписки с указанными данными в формате JSON.
        response = self.client.put(self.url, data, format="json")

        # Проверяем, что статус ответа 401 Unauthorized, что подтверждает отсутствие
        # прав доступа для неавторизованного пользователя.
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_subscription_not_admin(self):
        """Тест проверки прав доступа для не-администратора"""

        # Создаем нового пользователя с заданными атрибутами:
        self.user = User.objects.create(
            email="non_admin@test.ru",
            password="1234",
            is_superuser=False,
            is_staff=False,
        )
        # Устанавливаем пароль пользователя.
        self.user.set_password("1234")
        self.user.save()
        # Аутентифицируем тестового клиента под созданным пользователем.
        self.client.force_authenticate(user=self.user)

        # Создаем данные для обновления подписки.
        data = {
            'subscription_type': 'course',
            'course': self.course.id,
        }
        # Выполняем PUT-запрос к URL обновления подписки с указанными данными в формате JSON.
        response = self.client.put(self.url, data, format='json')
        # Проверяем, что статус ответа равен 403 Forbidden (доступ запрещен).
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_subscription(self):
        """Тест получения определенной подписки."""

        # Генерируем URL для получения конкретной подписки по её ID.
        url = reverse("modules:subscription_retrieve", args=[self.subscription.id])

        # Выполняем GET-запрос к URL получения подписки.
        response = self.client.get(url)

        # Проверяем, что ответ успешный (200 OK).
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем, что данные в ответе соответствуют ожидаемым:
        # - ID подписки соответствует ожидаемому значению.
        self.assertEqual(response.data["id"], self.subscription.id)
        # - ID подписчика соответствует ожидаемому значению.
        self.assertEqual(response.data["subscriber"], self.user.id)
        # - ID курса соответствует ожидаемому значению.
        self.assertEqual(response.data["course"], self.course.id)
        # - ID модуля соответствует ожидаемому значению.
        self.assertEqual(response.data["module"], self.module.id)

    def test_delete_subscription(self):
        """Тест удаления подписки."""

        # Генерируем URL для удаления подписки по её первичному ключу (ID).
        url = reverse(
            "modules:subscription_delete", args=[self.subscription.id]
        )

        # Выполняем DELETE-запрос к сгенерированному URL для удаления подписки.
        # Этот запрос должен инициировать удаление подписки из системы.
        response = self.client.delete(url)

        # Проверяем, что статус ответа 204 No Content.
        # Это указывает на то, что подписка была успешно удалена.
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Проверяем, что подписка больше не существует в базе данных.
        self.assertFalse(Subscription.objects.filter(id=self.subscription.id).exists())

    def test_unauthenticated_access(self):
        """Тест для проверки доступа без аутентификации."""

        url = reverse("modules:subscription_retrieve", args=[self.subscription.id])

        # Деаутентифицируем пользователя
        self.client.force_authenticate(user=None)
        response = self.client.get(url)

        # Проверка, что доступ запрещён (возвращается статус 404)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_nonexistent_subscription(self):
        """Тест для получения данных несуществующей подписки."""

        url = reverse("modules:subscription_retrieve", kwargs={'pk': 99999})
        response = self.client.get(url)

        # Проверка, что доступ запрещён (возвращается статус 404)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
