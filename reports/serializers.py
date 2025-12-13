"""Reports app serializers."""
from rest_framework import serializers
from reports.models import Alert


class AlertSerializer(serializers.ModelSerializer):
    """Serializer for Alert."""
    title = serializers.CharField(
        max_length=200,
        help_text="Alert title"
    )
    message = serializers.CharField(
        help_text="Detailed alert message"
    )
    alert_type = serializers.CharField(
        max_length=20,
        help_text="Alert type: 'danger', 'warning', 'success', or 'info'"
    )
    is_read = serializers.BooleanField(
        default=False,
        help_text="Whether the user has read this alert"
    )

    class Meta:
        model = Alert
        fields = [
            'id', 'user', 'title', 'message', 'alert_type',
            'is_read', 'related_category', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
        extra_kwargs = {
            'related_category': {'help_text': 'Category ID this alert is related to (optional)'}
        }
