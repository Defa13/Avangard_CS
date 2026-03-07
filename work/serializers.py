from rest_framework import serializers
from .models import WorkShift

class WorkShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkShift
        fields = [
            'id',
            'employee',
            'date',
            'start_time',
            'end_time',
            'hours_worked',
            'day_type',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['hours_worked', 'created_at', 'updated_at']
        
        
    def validate(self, data):
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        day_type = data.get('day_type')

        if day_type == "работа":
            if not start_time or not end_time:
                raise serializers.ValidationError("Для рабочего дня необходимо указать время начала и окончания работы.")
            if start_time >= end_time:
                raise serializers.ValidationError("Время начала работы должно быть раньше времени окончания.")
        return data