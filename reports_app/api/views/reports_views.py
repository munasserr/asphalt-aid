from rest_framework import viewsets, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from reports_app.models import Report
from reports_app.api.serializers.reports import ReportSerializer
from ai_service.pothole_classifier import predict_severity
import logging

logger = logging.getLogger(__name__)


class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return only the reports created by the logged-in user"""
        return Report.objects.filter(user=self.request.user).order_by("-created_at")

    def list(self, request, *args, **kwargs):
        """List all reports for the authenticated user"""
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(
                {
                    "detail": f"Retrieved {len(serializer.data)} reports successfully",
                    "count": len(serializer.data),
                    "reports": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"detail": f"An error occurred while retrieving reports: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def create(self, request, *args, **kwargs):
        """Create a new report with AI severity analysis"""
        try:
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                report = serializer.save(user=request.user)

                if report.image:
                    logger.info(
                        f"Image detected for report {report.id}: {report.image.path}"
                    )
                    logger.info("Calling AI prediction...")
                    try:
                        severity = predict_severity(report.image.path)
                        logger.info(f"AI predicted severity: {severity}")

                        report.severity = severity
                        report.save(update_fields=["severity"])
                        logger.info(
                            f"✓ Report {report.id} severity updated to {severity} by AI analysis"
                        )

                    except Exception as ai_error:
                        logger.error(
                            f"✗ AI prediction failed for report {report.id}: {str(ai_error)}"
                        )

                response_serializer = self.get_serializer(report)
                return Response(
                    {
                        "detail": "Report created successfully"
                        + (" with AI severity analysis" if report.image else ""),
                        "report": response_serializer.data,
                    },
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {"detail": "Validation errors", "errors": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            return Response(
                {"detail": f"An error occurred while creating report: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def retrieve(self, request, *args, **kwargs):
        """Retrieve a specific report"""
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(
                {"detail": "Report retrieved successfully", "report": serializer.data},
                status=status.HTTP_200_OK,
            )
        except Report.DoesNotExist:
            return Response(
                {"detail": "Report not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"detail": f"An error occurred while retrieving report: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def update(self, request, *args, **kwargs):
        """Update a report (PUT) - Only allow updating static fields"""
        try:
            instance = self.get_object()

            if instance.user != request.user:
                return Response(
                    {"detail": "You can only update your own reports"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            allowed_fields = ["description", "address", "name"]
            filtered_data = {
                key: value
                for key, value in request.data.items()
                if key in allowed_fields
            }

            attempted_fields = set(request.data.keys())
            non_allowed_fields = attempted_fields - set(allowed_fields)
            if non_allowed_fields:
                return Response(
                    {
                        "detail": f"Only {', '.join(allowed_fields)} fields can be updated",
                        "invalid_fields": list(non_allowed_fields),
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer = self.get_serializer(instance, data=filtered_data)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "detail": "Report updated successfully",
                        "report": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"detail": "Validation errors", "errors": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Report.DoesNotExist:
            return Response(
                {"detail": "Report not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"detail": f"An error occurred while updating report: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def partial_update(self, request, *args, **kwargs):
        """Partially update a report (PATCH) - Only allow updating static fields"""
        try:
            instance = self.get_object()

            if instance.user != request.user:
                return Response(
                    {"detail": "You can only update your own reports"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            allowed_fields = ["description", "address", "name"]
            filtered_data = {
                key: value
                for key, value in request.data.items()
                if key in allowed_fields
            }

            attempted_fields = set(request.data.keys())
            non_allowed_fields = attempted_fields - set(allowed_fields)
            if non_allowed_fields:
                return Response(
                    {
                        "detail": f"Only {', '.join(allowed_fields)} fields can be updated",
                        "invalid_fields": list(non_allowed_fields),
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer = self.get_serializer(instance, data=filtered_data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "detail": "Report updated successfully",
                        "report": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"detail": "Validation errors", "errors": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Report.DoesNotExist:
            return Response(
                {"detail": "Report not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"detail": f"An error occurred while updating report: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def destroy(self, request, *args, **kwargs):
        """Delete a report"""
        try:
            instance = self.get_object()


            if instance.user != request.user:
                return Response(
                    {"detail": "You can only delete your own reports"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            instance.delete()
            return Response(
                {"detail": "Report deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Report.DoesNotExist:
            return Response(
                {"detail": "Report not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"detail": f"An error occurred while deleting report: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
