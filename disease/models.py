from django.db import models


# Create your models here.
class Disease(models.Model):
    disease_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

    def find(disease_id: int):
        return Disease.objects.filter(disease_id=disease_id).first()
