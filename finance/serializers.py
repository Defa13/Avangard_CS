from rest_framework import serializers
from .models import Payroll


class PayrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payroll
        fields = [
            'id',
            'employee',
            'period_start',
            'period_end',
            'worked_hours',
            'base_salary',
            'bonus',
            'penalty',
            'total_amount',
            'is_paid',
            'paid_at',
            'created_at',
        ]
        read_only_fields = [
            'worked_hours',
            'base_salary',
            'total_amount',
            'paid_at',
            'created_at',
        ]

    def validate(self, attrs):
        start = attrs.get('period_start')
        end = attrs.get('period_end')

        if start and end and start > end:
            raise serializers.ValidationError(
                "period_start не может быть больше period_end"
            )

        return attrs
