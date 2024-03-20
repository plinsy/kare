from django.db import models

from disease.models import Disease
from drug.models import Drug


# Create your models here.
class Treatment(models.Model):
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    number = models.IntegerField()
    price = models.FloatField()

    def __str__(self) -> str:
        return (
            "Treatment["
            + str(self.disease)
            + " => "
            + "("
            + self.number.__str__()
            + ") * "
            + str(self.drug)
            + " : "
            + self.price.__str__()
            + "]"
        )
