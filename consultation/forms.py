from django import forms

from disease.models import Disease
from symptom.models import Symptom


class ConsultationForm(forms.Form):
    name = forms.CharField(max_length=255, required=True, label="Nom", initial="Nobody")
    selected_diseases = forms.ModelMultipleChoiceField(
        queryset=Symptom.objects.all(),
        widget=forms.Select(),
        label="Quels sont vos symptômes?",
    )
    disease_values = forms.IntegerField(
        min_value=0, max_value=50, label="", required=False
    )
