from django.db import models
from drug.models import Drug
from effect.models import Effect
from symptom.models import Symptom

from treatment.models import Treatment


# Create your models here.
class Diagnostic(models.Model):
    name = models.CharField(max_length=255)
    nausea = models.IntegerField()
    headache = models.IntegerField()
    bellyache = models.IntegerField()

    def __str__(self) -> str:
        return (
            self.nausea.__str__()
            + "-"
            + self.headache.__str__()
            + "-"
            + self.bellyache.__str__()
            + " "
            + self.name
        )

    def get_treatments_for(self, symptom: Symptom) -> list[Treatment]:
        result = []
        for drug in Drug.objects.all():
            t = Treatment(disease=symptom.disease, drug=drug, price=0)
            effect = Effect.find(drug, symptom.disease)
            ### Pour aténuer les symptômes d'une maladie,
            ### c-à-d pour avoir le nombre de médicaments nécessaire
            ### pour éliminer totalement les symptômes
            ### On résoud l'équation (e)*n + s = 0
            ### où
            ###     e: l'effet du traitement sur la maladie, ex: -2
            ###     s: le niveau de la maladie, ex: 15
            ###     n: le nombre de traitement nécessaire. n est un entier
            ### N.B.: il est possible qu'un traitement ne résoud pas le problème
            ### Dans ce cas, n n'a pas de valeur
            # Il faut que l'effet soit négatif pour réduire la maladie
            # Et il faut que le symptome soit positif pour qu'on puisse lui appliquer un traitment
            if effect != None and effect.value < 0 and symptom.name > 0:
                t.number = round(-(symptom.name) / effect.value)
                t.price += drug.price * t.number
                result.append(t)
                # Treatment.objects.create(t)
            else:
                pass

        return result

    def get_all_treatments_for(self, symptoms: list[Symptom]) -> list[list[Treatment]]:
        result = []
        for symptom in symptoms:
            sub_treatments = self.get_treatments_for(symptom)
            if len(sub_treatments) > 0:
                result.append(sub_treatments)

        results: list[list[Treatment]] = product(*result)

        return results


def product(*args):
    if not args:
        return [()]
    result = []
    for prod in args[0]:
        for rest in product(*args[1:]):
            result.append((prod,) + rest)
    return result
