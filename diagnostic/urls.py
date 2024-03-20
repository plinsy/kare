from django.urls import path
from . import views


urlpatterns = [
    path("", views.DiagnosticView.as_view(), name="diagnostic"),
    path("create", views.DiagnosticCreateView.as_view(), name="diagnostic_create"),
    path(
        "<int:pk>/result",
        views.DiagnosticDetailView.as_view(),
        name="diagnostic_details",
    ),
    path("result", views.DiagnosticResultView.as_view(), name="diagnostic_result"),
]
