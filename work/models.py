from django.db import models
from employees.models import Employee
from datetime import datetime, timedelta


class WorkShift(models.Model):
    DAY_TYPE_CHOICES = (
        ("работа", "Рабочий день"),
        ("отпуск", "Отпуск"),
        ("больничный", "Больничный"),
        ("выходной", "Выходной"),
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="work_shifts"
    )

    date = models.DateField()

    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    hours_worked = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        editable=False
    )

    day_type = models.CharField(
        max_length=20,
        choices=DAY_TYPE_CHOICES,
        default="работа"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Рабочая смена"
        verbose_name_plural = "Рабочие смены"

    def save(self, *args, **kwargs):
        if self.start_time and self.end_time and self.day_type == "работа":
            start = datetime.combine(self.date, self.start_time)
            end = datetime.combine(self.date, self.end_time)

            if end < start:
                end += timedelta(days=1)

            diff = end - start
            self.hours_worked = round(diff.total_seconds() / 3600, 2)
        else:
            self.hours_worked = 0

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee} — {self.date}"
