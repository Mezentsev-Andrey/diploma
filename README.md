# Проект "Образовательные модули"

Данный проект представляет собой контейнерную версию Django-приложения “Образовательные модули”.

## О проекте

Бэкенд обеспечивает API для работы просмотра, создания, редактирования, удаления образовательных модулей и связанных с ними курсов и уроков. 

## Возможности

- Регистрация и авторизация пользователей;
- Создание, чтение, обновление и удаление образовательных модулей в соответствии с поставленными задачами пользователей;
- Просмотр списка образовательных модулей и связанных с ними курсами и уроками с пагинацией;
- Просмотр списка общедоступных образовательных модулей, связанных курсов и уроков;
- Интеграция с рассылкой электронной почты пользователям уведомлений об изменении образовательного модуля. 

## Технологии

- Python;
- Django (Django REST framework, Celery);
- PostgreSQL (БД для хранения данных);
- Docker.

## Запуск проекта

1. Установите зависимости:
    - `pip install -r requirements.txt`

2. Создайте файл `.env` в корневой директории и заполните необходимые переменные окружения:
    - POSTGRES_DB=`"имя базы данных"`;
    - POSTGRES_USER=`"пользователь базы данных"`;
    - POSTGRES_PASSWORD=`"пароль базы данных"`;
    - POSTGRES_PORT=`"порт базы данных"`;
    - POSTGRES_HOST=`"хост базы данных"`.
   
   2.1. Настройка электронной почты с которой будут приходить уведомления согласно требуемых настроек:
    - EMAIL_HOST=`"хост электронной почты"`;
    - EMAIL_PORT=`"порт электронной почты"`;
    - EMAIL_HOST_USER=`"пользователь электронной почты"`;
    - EMAIL_HOST_PASSWORD=`"пароль электронной почты"`;
    
   2.2. Настройка Celery:
   - CELERY_BROKER_URL=`"URL брокера Celery"`;
   - CELERY_RESULT_BACKEND=`"URL бэкенда Celery"`.

3. Примените миграции:
    - `python manage.py migrate`

4. Запустите сервер:
    - `python manage.py runserver`

5. Запустите Celery для обработки отложенных задач:
    - `celery -A config worker -l INFO -P eventlet`
    - `celery -A config beat -l INFO`

6. Запуск приложения:
    - Заполнение базы данных произведено в админке. Загруженные данные представлены по адресу: modules/fixtures/all_data.json, modules/fixtures/modules_data.json; users/fixtures/users_data.json. Для их загрузки в базу данных проекта воспользуйтесь командой: `python manage.py loaddatautf8 modules_data.json`
    - Для выгрузки данных из базы данных проекта используйте команду: `python manage.py dumpdatautf8 modules --output modules/fixtures/modules_data.json` (в данном примере команды приведена выгрузка всех данных из приложения modules.)
    - Создать суперпользователя кастомной командой `python manage.py csu`.

7. Виды запросов в Postman: 

   Запросы в Postman для образовательного модуля:
    - POST: http://localhost:8000/modules/create/ (заполнить тело, выбрав параметры 'raw' и 'json'; поля: name, description);
    - GET: (получить список модулей): http://localhost:8000/modules/;
    - GET: (получить конкретный модуль): http://localhost:8000/modules/retrieve/<pk модуля>/;
    - PUT: http://localhost:8000/modules/update/<pk модуля>/ (заполнить тело, выбрав параметры 'raw' и 'json');
    - DELETE: http://localhost:8000/modules/delete/<pk модуля>/.
   
   Запросы в Postman для курса:
    - POST: http://localhost:8000/course/create/ (заполнить тело, выбрав параметры 'raw' и 'json'; поля: name, description);
    - GET: (получить список курсов): http://localhost:8000/course/;
    - GET: (получить конкретный курс): http://localhost:8000/course/retrieve/<pk курса>/;
    - PUT: http://localhost:8000/course/update/<pk курса> (заполнить тело, выбрав параметры 'raw' и 'json');
    - DELETE: http://localhost:8000/course/delete/<pk курса>.
   
    Запросы в Postman для урока:
    - POST: `http://localhost:8000/lesson/create/ (заполнить тело, выбрав параметры 'raw' и 'json', поля: name, description, course);
    - GET (получить список уроков): http://localhost:8000/lesson/;
    - GET (получить конкретный урок): http://localhost:8000/lesson/retrieve/<pk урока>/;
    - PATCH: http://localhost:8000/lesson/update/<pk урока>;
    - DELETE: http://localhost:8000/lesson/delete/<pk урока>.
8. Регистрация нового пользователя: 
   - POST: http://localhost:8000/users/user/ (заполнить тело, выбрав параметры 'raw' и 'json', поля: email, password).
9. После регистрации пользователя нужно войти в приложение с помощью логина и пароля сделав соответствующий запрос:
   - POST: http://localhost:8000/users/login/

## Документация API

Документация API доступна после запуска сервера по адресам: http://localhost:8000/redoc/ и http://localhost:8000/swagger/

## Запуск проекта с использованием Docker
  - Используйте файлы Dockerfile и docker-compose.yml. При необходимости внесите в них требуемые изменения;
  - Соберите образ с помощью команды: `docker-compose build`;
  - Запустите контейнеры с помощью команды: `docker-compose up`;
  - Управление контейнерами: Для остановки и удаления контейнеров используйте Ctrl + C в терминале, где запущен docker-compose up. Для остановки контейнеров и удаления созданных ресурсов выполните команду: `docker-compose down`;
  - Если при запуске контейнера добавить флаг -d, процесс запустится в фоновом режиме (как демон). В случае, если к команде добавить флаг --build, то перед запуском выполнится сборка. В итоге команда будет выглядеть так: `docker-compose up -d --build`.
