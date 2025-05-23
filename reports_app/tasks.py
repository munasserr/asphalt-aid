from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


@shared_task
def analyze_report_image(report_id):
    try:
        from reports_app.models import Report
        from ai_service.pothole_classifier import classifier

        report = Report.objects.get(id=report_id)

        if report.image:
            image_path = report.image.path
            severity = classifier.predict_severity(image_path)

            report.severity = severity
            report.save(update_fields=["severity"])

            logger.info(
                f"Report {report_id} severity updated to {severity} based on AI analysis"
            )
            return f"Report {report_id} analyzed successfully. Severity: {severity}"
        else:
            logger.warning(f"Report {report_id} has no image to analyze")
            return f"Report {report_id} has no image"

    except Exception as e:
        logger.error(f"Error analyzing report {report_id}: {str(e)}")
        return f"Error analyzing report {report_id}: {str(e)}"
