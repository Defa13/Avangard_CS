from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from openpyxl import Workbook
from django.http import HttpResponse
from django.db.models import Sum
from datetime import datetime
from rest_framework.permissions import AllowAny


from .models import Payroll
from .serializers import PayrollSerializer
from users.permissions import IsAdmin, IsBoss, IsOperator
from logs.models import Log

class PayrollListCreateView(generics.ListCreateAPIView):
    queryset = Payroll.objects.all()
    serializer_class = PayrollSerializer
    permission_classes = [IsAdmin | IsBoss]


class PayrollDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payroll.objects.all()
    serializer_class = PayrollSerializer
    permission_classes = [IsAdmin | IsBoss]


class PayrollPayView(APIView):
    permission_classes = [IsAdmin | IsBoss]

    def post(self, request, pk):
        payroll = Payroll.objects.get(pk=pk)

        if payroll.is_paid:
            return Response(
                {'error': 'Зарплата уже выплачена'},
                status=status.HTTP_400_BAD_REQUEST
            )

        payroll.is_paid = True
        payroll.paid_at = timezone.now()
        payroll.save()
        
        Log.objects.create(
            user=self.request.user,
            action=f"Выплачена зарплата: {payroll.employee}",
        )

        return Response({'status': 'Зарплата выплачена'})


class MyPayrollListView(generics.ListAPIView):
    serializer_class = PayrollSerializer
    permission_classes = [IsOperator | IsAdmin | IsBoss]

    def get_queryset(self):
        return Payroll.objects.filter(
            employee__user=self.request.user
        )


from drf_spectacular.utils import extend_schema, OpenApiParameter

@extend_schema(
    parameters=[
        OpenApiParameter("start", str, description="Дата начала YYYY-MM-DD"),
        OpenApiParameter("end", str, description="Дата конца YYYY-MM-DD"),
    ],
    responses={200: None},
)
class PayrollExportExcelView(APIView):
    permission_classes = [IsAdmin | IsBoss]

    def get(self, request):
        """
        GET-параметры:
        start=YYYY-MM-DD
        end=YYYY-MM-DD
        """

        start_date = request.GET.get("start")
        end_date = request.GET.get("end")

        # Проверка дат
        if not start_date or not end_date:
            return HttpResponse("Параметры start и end обязательны", status=400)

        try:
            start = datetime.strptime(start_date, "%Y-%m-%d").date()
            end = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            return HttpResponse("Неверный формат даты, нужен YYYY-MM-DD", status=400)

        # Берём payroll только за выбранный период и только выплаченные
        payrolls = Payroll.objects.filter(
            period_start__gte=start,
            period_end__lte=end,
            is_paid=True
        ).order_by("employee__id", "period_start")

        # Создаём Excel
        wb = Workbook()
        sheet = wb.active
        sheet.title = "Зарплаты"

        # Заголовки на русском
        sheet.append([
            "Сотрудник",
            "Период",
            "Отработано часов",
            "Ставка в час",
            "Премия",
            "Штраф",
            "Итого",
            "Выплачено",
        ])

        # Заполняем строки
        for p in payrolls:
            sheet.append([
                str(p.employee),
                f"{p.period_start} – {p.period_end}",
                float(p.worked_hours),
                float(p.base_salary),
                float(p.bonus),
                float(p.penalty),
                float(p.total_amount),
                "ДА" if p.is_paid else "НЕТ",
            ])

        # Формируем ответ для скачивания
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = f'attachment; filename="зарплаты_{start}_{end}.xlsx"'
        wb.save(response)
        
        # Log 
        Log.objects.create(
            user=self.request.user,
            action=f"Экспортированы зарплаты за период {start} – {end}",
        )
        
        return response