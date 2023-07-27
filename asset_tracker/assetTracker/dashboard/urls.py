from django.urls import path
from dashboard.views import PieChartHandler, BarChartHandler

urlpatterns = [
    path("pie-chart", PieChartHandler.as_view(), name="pie-chart"),
    path("bar-chart", BarChartHandler.as_view(), name="bar-chart")
]