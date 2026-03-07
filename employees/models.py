from django.db import models
from users.models import CustomUser
from django.conf import settings


class Employee(models.Model):
    STATUS_CHOICES = (
        ("работает", "Работает"),
        ("уволен", "Уволен"),
        ("в отпуске", "В отпуске"),
        ("больничный", "Больничный"),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="employee",
        null=True,
        blank=True
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    # должность и отдел
    position = models.CharField(max_length=100, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="работает"
    )

    base_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=17000.00
    )

    # руководитель сотрудника
    manager = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subordinates"
    )

    # даты приема и увольнения
    hire_date = models.DateField()
    fired_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.position})"
    

