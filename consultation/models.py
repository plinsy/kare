# Create your models here.
from typing import Any, List, Optional

from app import Effect
from drug.models import Drug
from symptom.models import Symptom


class Object:
    name: str

    def __init__(self, name) -> None:
        self.name = name

    def __str__(self) -> str:
        return f"{self.__class__}<{self.name}>"

    def __repr__(self) -> str:
        return self.__str__()


class Symptomable(Object):
    effects: List["Effect"]

    def __init__(self) -> None:
        self.effects = []

    def hasSymptom(self, symptom_id: int):
        for e in self.effects:
            if e.symptom_id == symptom_id:
                return True
        return False


class Patient(Symptomable):
    id: int = 0
    patient_id: int
    treatments: List["Treatment"]

    def __init__(self, name: str):
        super().__init__()
        Patient.id += 1
        self.patient_id = Patient.id
        self.name = name
        self.treatments = []

    def __str__(self) -> str:
        return f"Patient({self.patient_id} :: name={self.name})"

    def addSymptom(self, symptom_id: int, value: float):
        self.effects.append(
            Effect(
                item=self,
                symptom_id=symptom_id,
                value=value,
            )
        )

    def getTreatments(self, effect: "Effect") -> List["Treatment"]:
        result: List["Treatment"] = []
        treatment_id: int = 0

        drugs = effect.getDrugs()

        if len(drugs) == 0:
            print(f"There is no drug for: {effect.getSymptom()}")
            return []

        for drug in drugs:
            treatment_id += 1
            t = Treatment(
                drug=drug,
                patient_id=self.patient_id,
                treatment_id=treatment_id,
            )
            drug_effect = drug.findEffect(effect)
            ### Pour aténuer les symptômes d'une maladie,
            ### c-à-d pour avoir le nombre de médicaments nécessaire
            ### pour éliminer totalement les symptômes
            ### On résoud l'équation (e)*n + s = 0
            ### n = -s / (e)
            ### où
            ###     e: l'effet du traitement sur la maladie, ex: -2
            ###     s: la valeur du symptome du patient, ex: 15
            ###     n: le nombre de traitement nécessaire. n est un entier
            ### N.B.: il est possible qu'un traitement ne résoud pas le problème
            ### Dans ce cas, n n'a pas de valeur
            # Il faut que l'effet soit négatif pour réduire la maladie
            # Et il faut que le symptome soit positif pour qu'on puisse lui appliquer un traitment
            if drug_effect == None or drug_effect.value >= 0 or effect.value < 0:
                print(f"Drug effect: {drug_effect}")
                print(f"effect: {effect}")
            else:
                t.number = round(-(effect.value) / drug_effect.value)
                t.price += round(drug.price * t.number, 2)
                result.append(t)

        return result

    def getAllTreatments(self) -> List[List["Treatment"]]:
        if len(self.effects) <= 0:
            print(f"{self.name} n'est pas malade")
            return []
        result = []
        for effect in self.effects:
            sub_treatments = self.getTreatments(effect)
            if len(sub_treatments) > 0:
                result.append(sub_treatments)
        return result

    def filterTreatments(
        self,
        treatments_list: List[List["Treatment"]],
    ) -> List[List["Treatment"]]:
        final_treatments_list = []
        for initial_treatments in treatments_list:
            new_treatments = []
            for treatment in initial_treatments:
                if treatment.number > 0:
                    treatment_in_new_list = getTreatment(new_treatments, treatment)
                    if treatment_in_new_list is None:
                        new_treatments.append(treatment)
                    else:
                        if treatment_in_new_list.number < treatment.number:
                            new_treatments.remove(treatment_in_new_list)
                            new_treatments.append(treatment)
            if new_treatments not in final_treatments_list:
                final_treatments_list.append(new_treatments)
        return final_treatments_list


class Treatment(Object):
    patient_id: int
    treatment_id: int
    drug: "Drug"
    number: int
    price: float

    def __init__(
        self, patient_id: int, treatment_id: int, drug: "Drug", number: int = 0
    ) -> None:
        self.patient_id = patient_id
        self.treatment_id = treatment_id
        self.drug = drug
        self.setNumber(number)

    def setNumber(self, number: int):
        self.number = number
        self.price = number * self.drug.price

    def __str__(self) -> str:
        return f"Treatment(\n\t\t{self.drug} * {self.number} = {self.price}\n\t)"


class Disease(Object):
    disease_id: int

    def __init__(self, disease_id: int, name: str) -> None:
        self.disease_id = disease_id
        self.name = name

    def __str__(self) -> str:
        return f"Disease({self.disease_id} :: name={self.name})"


def product(*args):
    if not args:
        return [()]
    result = []
    for prod in args[0]:
        for rest in product(*args[1:]):
            result.append((prod,) + rest)
    return result


def getTreatment(
    treatments: List["Treatment"], treatment_to_find: "Treatment"
) -> "Treatment":
    for treatment in treatments:
        if treatment.treatment_id == treatment_to_find.treatment_id:
            return treatment
    return None


def getMin(treatments: List["Treatment"]) -> Optional["Treatment"]:
    if not treatments:
        return None

    min_treatment = treatments[0]

    for treatment in treatments:
        if treatment.price < min_treatment.price:
            min_treatment = treatment

    return min_treatment


def get_price(treatments: List["Treatment"]) -> float:
    price = 0
    for treatment in treatments:
        price += treatment.price
    return price


def get_min(treatments_list: List[List["Treatment"]]) -> List["Treatment"]:
    if not treatments_list:
        return None

    min_treatment = treatments_list[0]
    minimum_price = get_price(min_treatment)

    for treatments in treatments_list:
        if get_price(treatments) < minimum_price:
            min_treatment = treatments
            minimum_price = get_price(min_treatment)

    return min_treatment


class Consultation:
    patient: "Patient"
    symptoms: List["Symptom"]

    def __init__(self, patient: "Patient", symptoms: List["Symptom"]):
        self.patient = patient
        self.symptoms = symptoms

    def evaluate(self) -> dict[str, Any]:
        if len(self.symptoms) == 0:
            print(f"This patient has no symptoms")
            return []

        self.patient.addSymptom(1, 5)
        self.patient.addSymptom(2, 15)
        self.patient.addSymptom(3, 10)
        self.patient.addSymptom(4, 5)
        self.patient.addSymptom(5, 5)
        self.patient.addSymptom(6, 5)
        self.patient.addSymptom(7, 5)
        self.patient.addSymptom(8, 5)
        self.patient.addSymptom(9, 5)
        self.patient.addSymptom(10, 5)

        medecins = self.patient.getAllTreatments()

        result: List[List[Treatment]] = product(*medecins)

        result = self.patient.filterTreatments(result)

        # print("Here is the List of possible cure:")
        # for treatments in result:
        #     print("Treatment")
        #     for t in treatments:
        #         print(f"\t{t}")

        min = get_min(result)

        # print("Here is the less expensive treatment:")
        # for t in min:
        #     print(f"\t{t}")

        return {
            "result": result,
            "min": min,
        }
