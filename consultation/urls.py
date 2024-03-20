from django.urls import path

from consultation import views


urlpatterns = [
    path("", views.ConsultationView.as_view(), name="consultation_index"),
]
