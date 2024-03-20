from typing import Any
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView

from consultation.forms import ConsultationForm


# Create your views here.
class ConsultationView(TemplateView):
    form_class = ConsultationForm
    template_name = "index.html"

    def get_success_url(self):
        return reverse("diagnostic_result")

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class
        context["result"] = None
        return context
