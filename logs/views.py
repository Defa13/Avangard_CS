from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.generics import ListAPIView
from .models import Log
from .serializers import LogSerializer
from users.permissions import IsAdmin, IsBoss

class LogListView(ListAPIView):
    queryset = Log.objects.all().order_by('-created_at')
    serializer_class = LogSerializer
    permission_classes = [IsAdmin | IsBoss]
