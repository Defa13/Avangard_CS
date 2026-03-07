from rest_framework import serializers
from .models import EmployeeMetrics


class EmployeeMetricsSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(
        source="employee.full_name",
        read_only=True
    )

    class Meta:
        model = EmployeeMetrics
        fields = (
            "id",
            "employee",
            "employee_name",
            "period",
            "quality",
            "breaks_pct",
            "cvd",
            "hold_pct",
        )
