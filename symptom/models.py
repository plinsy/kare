from typing import List
from django.db import models


# Create your models here.
class Symptom(models.Model):
    name = models.CharField(max_length=255)

    def find(symptom_id: int):
        return [
            symptom for symptom in Symptom.objects.all() if symptom.pk == symptom_id
        ][0]

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self) -> str:
        return f"Symptom({self.name})"
