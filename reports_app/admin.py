from django.contrib import admin
from reports_app.models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "name",
        "report_type",
        "get_severity_display",
        "status",
        "created_at",
    )
    list_filter = ("status", "report_type", "severity", "created_at")
    search_fields = ("user__username", "description", "address", "name")
    ordering = ("-created_at",)
    readonly_fields = ("severity", "created_at", "updated_at", "report_type")

    def get_severity_display(self, obj):
        return f"{obj.severity}/3 - {obj.get_severity_display()}"

    get_severity_display.short_description = "AI Severity"
