from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class Report(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("resolved", "Resolved"),
        ("rejected", "Rejected"),
    ]

    REPORT_TYPES = [
        ("pothole", "Pothole"),
        ("crack", "Crack"),
        ("road_sink", "Road Sink"),
        ("other", "Other"),
    ]

    SEVERITY_CHOICES = [
        (0, "No severity - Normal road"),
        (1, "Low - Minor issue"),
        (2, "Medium - Moderate damage"),
        (3, "High - Major damage"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reports")
    image = models.ImageField(upload_to="reports/")
    description = models.TextField()
    name = models.TextField()
    address = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    severity = models.IntegerField(
        default=1,
        choices=SEVERITY_CHOICES,
        validators=[MinValueValidator(0), MaxValueValidator(3)],
        help_text="Severity level determined by AI analysis of the uploaded image (0-3 scale)",
    )
    report_type = models.CharField(
        max_length=50, choices=REPORT_TYPES, default="pothole"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Report ({self.report_type}) by {self.user.username} - {self.status}"
