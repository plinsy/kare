from typing import List
from django.db import models

from disease.models import Disease
from drug.models import Drug
from symptom.models import Symptom

# from symptomable.models import Symptomable


# Create your models here.
class Effect(models.Model):
    # item = models.ForeignKey(Symptomable, on_delete=models.CASCADE)
    symptom = models.ForeignKey(Symptom, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)

    def find(drug: Drug, disease: Disease) -> "Effect":
        results = [
            effect
            for effect in Effect.objects.all()
            if effect.item == drug and effect.symptom == disease
        ]
        if results.__len__() == 0:
            return None
        return results[0]

    def getSymptom(self) -> "Symptom":
        return [
            symptom
            for symptom in Symptom.objects.all()
            if symptom.symptom_id == self.symptom_id
        ][0]

    def getDrugs(self) -> List["Drug"]:
        result = []
        for drug in Drug.objects.all():
            if drug.hasSymptom(self.symptom_id):
                result.append(drug)
        return result

    def __init__(
        self, item_id: int, item_type: str, symptom_id: int, value: float
    ) -> None:
        self.item_id = item_id
        self.item_type = item_type
        self.symptom_id = symptom_id
        self.value = value

    def __str__(self) -> str:
        symptom = self.getSymptom()
        return f"Effect({self.item_type}({self.item_id}) :: symptom={symptom} : value={self.value})"
