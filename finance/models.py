from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Sum
from employees.models import Employee
from work.models import WorkShift
from decimal import Decimal, ROUND_HALF_UP


class Payroll(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='payrolls'
    )

    period_start = models.DateField()
    period_end = models.DateField()

    worked_hours = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0
    )

    base_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    bonus = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    penalty = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('employee', 'period_start', 'period_end')
        verbose_name = "Зарплата"
        verbose_name_plural = "Зарплаты"


    def clean(self):
        if self.pk:
            old = Payroll.objects.get(pk=self.pk)
            if old.is_paid:
                raise ValidationError("Зарплата уже выплачена — изменения запрещены")


    def calculate_worked_hours(self):
        total = WorkShift.objects.filter(
            employee=self.employee,
            date__range=(self.period_start, self.period_end)
        ).aggregate(
            total=Sum('hours_worked')
        )['total'] or 0

        self.worked_hours = total
        return total


    def calculate_total_amount(self):
        total = (
            self.worked_hours * self.base_salary
            + self.bonus
            - self.penalty
        )
        # округляем до 2 знаков
        total = Decimal(total).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        self.total_amount = total
        return total


    def save(self, *args, **kwargs):
        if not self.pk:
            self.base_salary = self.employee.base_salary

        if not self.is_paid:
            self.calculate_worked_hours()
            self.calculate_total_amount()

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee} | {self.period_start} - {self.period_end}"

