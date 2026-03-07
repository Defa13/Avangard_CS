from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from .models import CustomUser
from .serializers import UserSerializer, LoginSerializer, LoginResponseSerializer
from drf_spectacular.utils import extend_schema
from .permissions import IsAdmin, IsBoss, IsOperator
from logs.models import Log

    
class LoginView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=LoginSerializer,
        responses=LoginResponseSerializer
    )
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if not user or not user.is_active:
            return Response(
                {"error": "Неверный логин или пароль"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "role": user.role
        })


class UserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin | IsBoss]
    
    def perform_create(self, serializer):
        serializer.save()

        Log.objects.create(
            user=self.request.user,
            action=f"Создан пользователь: {serializer.instance.username}",
        )


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin | IsBoss]


class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsOperator | IsBoss | IsAdmin]

    def get_object(self):
        return self.request.user

    
class ChangePasswordView(APIView):
    permission_classes = [IsOperator | IsBoss | IsAdmin]

    def post(self, request):
        user = request.user

        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not user.check_password(old_password):
            return Response(
                {"error": "Старый пароль неверен"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if len(new_password) < 8:
            return Response(
                {"error": "Пароль должен быть не менее 8 символов"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()

        return Response({"status": "Пароль изменён"})


class DeactivateUserView(APIView):
    permission_classes = [IsAdmin | IsBoss]

    def post(self, request, user_id):
        user = CustomUser.objects.get(id=user_id)
        user.is_active = False
        user.save()

        return Response({"status": "Пользователь деактивирован"})
    
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logged out"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
