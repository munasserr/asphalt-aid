from django.urls import path, include
from rest_framework.routers import DefaultRouter
from reports_app.api.views.reports_views import ReportViewSet

router = DefaultRouter()
router.register(r'reports', ReportViewSet, basename='report')

urlpatterns = [
    path('', include(router.urls)),
]