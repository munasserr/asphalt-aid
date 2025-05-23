from rest_framework import serializers
from reports_app.models import Report


class ReportSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)
    severity = serializers.IntegerField(
        read_only=True,
        help_text="Automatically determined by AI analysis of uploaded image",
    )

    class Meta:
        model = Report
        fields = "__all__"
        read_only_fields = ["user", "created_at", "updated_at", "status", "severity"]
