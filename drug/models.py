from django.db import models

# from effect.models import Effect


# Create your models here.
class Drug(models.Model):
    drug_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.FloatField()

    def __init__(self, drug_id: int, name: str, price: float) -> None:
        self.drug_id = drug_id
        self.name = name
        self.price = price

    def __str__(self) -> str:
        return f"Drug({self.drug_id} :: name={self.name}, price={self.price})"

    # def addSymptom(self, symptom_id: int, value: float):
    #     self.effects.append(
    #         Effect(
    #             item_id=self.drug_id,
    #             item_type="Drug",
    #             symptom_id=symptom_id,
    #             value=value,
    #         )
    #     )

    # def findEffect(self, effect: "Effect") -> "Effect":
    #     for eff in self.effects:
    #         if eff.symptom_id == effect.symptom_id:
    #             return eff
    #     return None
