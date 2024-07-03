from django.urls import path

from modules.apps import ModulesConfig
from modules.views import (LessonCreateAPIView, LessonDestroyAPIView,
                           LessonListAPIView, LessonRetrieveAPIView,
                           LessonUpdateAPIView, ModuleCreateAPIView,
                           ModuleDestroyAPIView, ModuleListAPIView,
                           ModuleRetrieveAPIView, ModuleUpdateAPIView,
                           SubscriptionListCreateView,
                           SubscriptionDetailView, CourseListAPIView, CourseCreateAPIView, CourseUpdateAPIView,
                           CourseDestroyAPIView, CourseRetrieveAPIView)

app_name = ModulesConfig.name

urlpatterns = [
    path("modules/create/", ModuleCreateAPIView.as_view(), name="module_create"),
    path("modules/", ModuleListAPIView.as_view(), name="module_list"),
    path("modules/<int:pk>/", ModuleRetrieveAPIView.as_view(), name="module_retrieve"),
    path(
        "modules/update/<int:pk>/", ModuleUpdateAPIView.as_view(), name="module_update"
    ),
    path(
        "modules/delete/<int:pk>/", ModuleDestroyAPIView.as_view(), name="module_delete"
    ),
    path("course/", CourseListAPIView.as_view(), name="course_list"),

    path("course/create/", CourseCreateAPIView.as_view(), name="course_create"),
    path("course/update/<int:pk>", CourseUpdateAPIView.as_view(), name="course_update"),
    path(
        "course/retrieve/<int:pk>",
        CourseRetrieveAPIView.as_view(),
        name="course_retrieve",
    ),
    path(
        "course/delete/<int:pk>", CourseDestroyAPIView.as_view(), name="course_delete"),

    path("lesson/", LessonListAPIView.as_view(), name="lesson_list"),
    path("lesson/create/", LessonCreateAPIView.as_view(), name="lesson_create"),
    path("lesson/update/<int:pk>", LessonUpdateAPIView.as_view(), name="lesson_update"),
    path(
        "lesson/retrieve/<int:pk>",
        LessonRetrieveAPIView.as_view(),
        name="lesson_retrieve",
    ),
    path(
        "lesson/delete/<int:pk>", LessonDestroyAPIView.as_view(), name="lesson_delete"
    ),
    path('subscriptions/', SubscriptionListCreateView.as_view(), name='subscription_list_create'),
    path('subscriptions/<int:pk>/', SubscriptionDetailView.as_view(), name='subscription_detail'),
]
