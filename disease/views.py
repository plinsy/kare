from django.shortcuts import render
from django.views.generic import ListView


from disease.models import Disease

# Create your views here.
class DiseaseListView(ListView):
    model = Disease
    template_name = "disease_list.html"
