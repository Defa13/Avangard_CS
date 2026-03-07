from rest_framework import generics
from rest_framework.exceptions import PermissionDenied

from .models import Employee
from .serializers import EmployeeSerializer
from users.permissions import IsAdmin, IsBoss, IsOperator
from logs.models import Log


class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdmin | IsBoss]

    def perform_create(self, serializer):
        serializer.save()
        
        Log.objects.create(
            user=self.request.user,
            action=f"Создан сотрудник: {serializer.instance.first_name} {serializer.instance.last_name}",
        )
        


class EmployeeDetailView(generics.RetrieveAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdmin | IsBoss]


class EmployeeUpdateView(generics.UpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdmin | IsBoss]


class MyEmployeeProfileView(generics.RetrieveAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = [IsOperator | IsBoss | IsAdmin]

    def get_object(self):
        user = self.request.user

        if not hasattr(user, "employee"):
            raise PermissionDenied("У вас нет профиля сотрудника")

        return user.employee


class FireEmployeeView(generics.UpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdmin | IsBoss]

    def perform_update(self, serializer):
        serializer.save(status="fired")

        Log.objects.create(
            user=self.request.user,
            action=f"Уволен сотрудник: {serializer.instance.first_name} {serializer.instance.last_name}",
        )