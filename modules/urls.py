from django.urls import path
from rest_framework.routers import DefaultRouter

from modules.apps import ModulesConfig
from modules.views import (
    CourseCreateAPIView,
    CourseDestroyAPIView,
    CourseListAPIView,
    CourseRetrieveAPIView,
    CourseUpdateAPIView,
    LessonCreateAPIView,
    LessonDestroyAPIView,
    LessonListAPIView,
    LessonRetrieveAPIView,
    LessonUpdateAPIView,
    SubscriptionCreateAPIView,
    SubscriptionDestroyAPIView,
    SubscriptionListAPIView,
    SubscriptionRetrieveAPIView,
    SubscriptionUpdateAPIView, ModuleViewSet,
)

app_name = ModulesConfig.name

router = DefaultRouter()
router.register(r"modules", ModuleViewSet, basename="modules")

urlpatterns = [
    path("course/", CourseListAPIView.as_view(), name="course_list"),
    path("course/create/", CourseCreateAPIView.as_view(), name="course_create"),
    path("course/update/<int:pk>", CourseUpdateAPIView.as_view(), name="course_update"),
    path(
        "course/retrieve/<int:pk>",
        CourseRetrieveAPIView.as_view(),
        name="course_retrieve",
    ),
    path(
        "course/delete/<int:pk>", CourseDestroyAPIView.as_view(), name="course_delete"
    ),
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
    path("subscription/", SubscriptionListAPIView.as_view(), name="subscription_list"),
    path(
        "subscription/create",
        SubscriptionCreateAPIView.as_view(),
        name="subscription_create",
    ),
    path(
        "subscription/update/<int:pk>",
        SubscriptionUpdateAPIView.as_view(),
        name="subscription_update",
    ),
    path(
        "subscription/retrieve/<int:pk>",
        SubscriptionRetrieveAPIView.as_view(),
        name="subscription_retrieve",
    ),
    path(
        "subscription/delete/<int:pk>",
        SubscriptionDestroyAPIView.as_view(),
        name="subscription_delete",
    ),
] + router.urls
