from django.urls import path
from . import views

urlpatterns = [
    path("", views.DiseaseListView.as_view(), name="disease")
]
