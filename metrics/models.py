from django.db import models

class EmployeeMetrics(models.Model):
    employee = models.ForeignKey(
        "employees.Employee",
        on_delete=models.CASCADE,
        related_name="metrics"
    )

    period = models.DateField(
        help_text="Первый день месяца",
        blank=False,
        null=False,
    )

    quality = models.FloatField(
        help_text="Качество %",
        blank=False,
        null=False,
    )

    breaks_pct = models.FloatField(
        help_text="% перерывов",
        blank=False,
        null=False,
    )

    cvd = models.FloatField(
        help_text="CVD показатель",
        blank=False,
        null=False,
    )

    hold_pct = models.FloatField(
        help_text="HOLD %",
        blank=False,
        null=False,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("employee", "period")
        verbose_name = "Метрики сотрудника"
        verbose_name_plural = "Метрики сотрудников"

    def __str__(self):
        return f"{self.employee} — {self.period}"

