from django.db import models
from django.conf import settings

class Log(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        verbose_name = "Лог Записи"
        verbose_name_plural = "Логи Записей"


    def __str__(self):
        return f"{self.user} - {self.action} at {self.created_at}"