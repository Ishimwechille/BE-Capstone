"""Reports app models."""
from django.db import models
from django.contrib.auth.models import User


class Alert(models.Model):
    """Automated alert/notification for user."""
    ALERT_TYPES = [
        ('danger', 'Danger'),
        ('success', 'Success'),
        ('tip', 'Tip'),
        ('info', 'Info'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alerts')
    title = models.CharField(max_length=200)
    message = models.TextField()
    alert_type = models.CharField(max_length=10, choices=ALERT_TYPES, default='info')
    is_read = models.BooleanField(default=False)
    related_category = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='Category that triggered this alert'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Alert'
        verbose_name_plural = 'Alerts'

    def __str__(self):
        return f"Alert ({self.get_alert_type_display()}): {self.title}"
