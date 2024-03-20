from typing import Any, List
from django.urls import reverse
from django.views.generic import TemplateView, CreateView, DetailView


from app import Effect
from consultation.models import Consultation, Patient
from diagnostic.forms import DiagnosticForm

from diagnostic.models import Diagnostic
from kare.mixins import JSONResponseMixin


# Create your views here.
class DiagnosticView(TemplateView):
    form_class = DiagnosticForm
    template_name = "index.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class
        context["result"] = None
        return context


class DiagnosticCreateView(CreateView):
    model = Diagnostic
    # form_class = DiagnosticForm
    template_name = "index.html"
    fields = "__all__"

    def get_success_url(self):
        return reverse("diagnostic_result")

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class
        context["result"] = {}
        return context


class DiagnosticDetailView(DetailView):
    model = Diagnostic
    form_class = DiagnosticForm
    template_name = "index.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class
        context["result"] = {}
        return context


class DiagnosticResultView(JSONResponseMixin, TemplateView):
    model = Diagnostic
    form_class = DiagnosticForm
    template_name = "index.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        print(self.request.GET)

        name: str = self.request.GET["name"]
        symptoms: str = self.request.GET["symptoms"]
        dict_symptoms: dict[int, int] = (
            symptoms.replace("'", "").replace("{", "").replace("}", "").split(", ")
        )

        patient = Patient(name=name)
        effects: List["Effect"] = []

        for str_symptom in dict_symptoms:
            if ":" in str_symptom:
                symptom_id_value = str_symptom.split(":")
                symptom_id: int = int(symptom_id_value[0])
                value: int = int(symptom_id_value[1])
                e = Effect(
                    item=patient,
                    symptom_id=symptom_id,
                    value=value,
                )
                effects.append(e)

        print(effects)

        consultation = Consultation(patient, effects)
        data = consultation.evaluate()

        # context = super().get_context_data(**kwargs)
        context = {}
        # context["form"] = self.form_class

        # Convert non-serializable objects to serializable format

        # serialized_data = serializers.serialize("json", data)
        serialized_data = self.serialize_object(data)

        context["data"] = serialized_data
        # context["symptoms"] = illness
        return context

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context["data"], **response_kwargs)
