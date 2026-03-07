from django.shortcuts import render
from rest_framework import generics
from .models import EmployeeMetrics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from openpyxl import Workbook
from datetime import datetime
from rest_framework.permissions import AllowAny

from users.permissions import IsAdmin, IsBoss, IsOperator
from .serializers import EmployeeMetricsSerializer
from logs.models import Log



class EmployeeMetricsListCreateView(generics.ListCreateAPIView):
    queryset = EmployeeMetrics.objects.all()
    serializer_class = EmployeeMetricsSerializer
    permission_classes = [IsAdmin | IsBoss]

    def get_queryset(self):
        qs = super().get_queryset()
        employee_id = self.request.query_params.get("employee")
        if employee_id:
            qs = qs.filter(employee_id=employee_id)
        return qs


class EmployeeMetricsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmployeeMetrics.objects.all()
    serializer_class = EmployeeMetricsSerializer
    permission_classes = [IsAdmin | IsBoss]


from drf_spectacular.utils import extend_schema, OpenApiParameter

@extend_schema(
    parameters=[
        OpenApiParameter("start", str, description="Дата начала YYYY-MM-DD"),
        OpenApiParameter("end", str, description="Дата конца YYYY-MM-DD"),
    ],
    responses={200: None},
)
class EmployeeMetricsExportExcelView(APIView):
    permission_classes = [IsBoss | IsAdmin]

    def get(self, request):
        """
        GET-параметры:
        start=YYYY-MM-DD
        end=YYYY-MM-DD
        employee=<id>  # необязательный фильтр
        """
        start_date = request.GET.get("start")
        end_date = request.GET.get("end")
        employee_id = request.GET.get("employee")

        # Проверка дат
        if not start_date or not end_date:
            return HttpResponse("Параметры start и end обязательны", status=400)
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d").date()
            end = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            return HttpResponse("Неверный формат даты, нужен YYYY-MM-DD", status=400)

        # Фильтруем метрики
        metrics = EmployeeMetrics.objects.filter(period__gte=start, period__lte=end)
        if employee_id:
            metrics = metrics.filter(employee_id=employee_id)

        metrics = metrics.order_by("employee__id", "period")

        # Создаём Excel
        wb = Workbook()
        sheet = wb.active
        sheet.title = "Метрики"

        # Заголовки
        sheet.append([
            "Сотрудник",
            "Период",
            "Качество",
            "Процент перерывов",
            "CVD",
            "Hold %",
        ])

        for m in metrics:
            sheet.append([
                str(m.employee),
                str(m.period),
                float(m.quality),
                float(m.breaks_pct),
                float(m.cvd),
                float(m.hold_pct),
            ])

        # Формируем ответ для скачивания
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = f'attachment; filename="метрики_{start}_{end}.xlsx"'
        wb.save(response)

        # Log
        Log.objects.create(
            user=self.request.user,
            action=f"Экспортированы метрики за период {start} – {end}",
        )

        return response