from django.urls import path
from .views import LineSpeedView, MetricsView

urlpatterns = [
    path("linespeed/", LineSpeedView.as_view(), name="line-speed"),
    path("metrics/", MetricsView.as_view(), name="metrics-all"),  # Returns metrics for all lines
    path("metrics/<int:lineid>/", MetricsView.as_view(), name="metrics"),
]
