from django import forms

class DiagnosticForm(forms.Form):
    name = forms.CharField(max_length=255, required=True, label="Nom", initial="Nobody")
    nausea = forms.IntegerField(min_value=0, max_value=50, required=True, label="Nausée", initial=0)
    headache = forms.IntegerField(min_value=0, max_value=50, required=True, label="Maux de tête", initial=0)
    bellyache = forms.IntegerField(min_value=0, max_value=50, required=True, label="Maux de ventre", initial=0)
    