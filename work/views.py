from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied

from .models import WorkShift
from .serializers import WorkShiftSerializer
from users.permissions import IsAdmin, IsOperator, IsBoss

class WorkListCreateView(generics.ListCreateAPIView):
    queryset = WorkShift.objects.all()
    serializer_class = WorkShiftSerializer
    permission_classes = [IsAdmin | IsBoss]
    

class WorkDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WorkShift.objects.all()
    serializer_class = WorkShiftSerializer
    permission_classes = [IsAdmin | IsBoss]
    
    
class MyWorkShiftListView(generics.ListAPIView):
    serializer_class = WorkShiftSerializer
    permission_classes = [IsOperator | IsBoss | IsAdmin]

    def get_queryset(self):
        user = self.request.user

        if not hasattr(user, "employee"):
            raise PermissionDenied("У вас нет профиля сотрудника")

        return WorkShift.objects.filter(employee=user.employee)

    
