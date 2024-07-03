from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.models import User
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Контроллер для работы с моделью User"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """Переопределение метода для сохранения хешированного пароля в БД"""

        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        password = serializer.data["password"]
        user = User.objects.get(pk=serializer.data["id"])
        user.set_password(password)
        user.is_active = True
        user.save()

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
