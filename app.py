from typing import Any, List, Optional
from rest_framework import serializers


DB: dict[str, List] = {
    "patients": [],
    "diseases": [],
    "drugs": [],
    "symptoms": [],
    "treatments": [],
}


class PatientSerializer(serializers.Serializer):
    patient_id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)


class DrugSerializer(serializers.Serializer):
    drug_id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    price = serializers.FloatField()


class TreatmentSerializer(serializers.Serializer):
    treatment_id = serializers.IntegerField()
    drug = DrugSerializer()
    # patient = PatientSerializer(instance="Patient")
    number = serializers.IntegerField()
    price = serializers.FloatField()


class Object:
    name: str

    def __init__(self, name) -> None:
        self.name = name

    def __str__(self) -> str:
        return f"{self.__class__}<{self.name}>"

    def __repr__(self) -> str:
        return self.__str__()


class Relation:
    def __repr__(self) -> str:
        return self.__str__()


class Symptomable(Object):
    effects: List["Effect"]

    def __init__(self) -> None:
        self.effects = []

    def addSymptom(self, symptom_id: int, value: float):
        self.effects.append(Effect(item=self, symptom_id=symptom_id, value=value))

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
        return f"Patient({self.patient_id} :: name={self.name}, treatments={self.treatments})"

    def getTreatments(self, effect: "Effect") -> List["Treatment"]:
        result = []
        treatment_id: int = 0

        drugs = effect.getDrugs()

        if len(drugs) == 0:
            print(f"There is no drug for: {effect.getSymptom()}")
            return []

        for drug in drugs:
            treatment_id += 1
            t = Treatment(
                patient=self,
                treatment_id=treatment_id,
                drug=drug,
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
            else:
                t.number = round(-(effect.value) / drug_effect.value)
                t.price += drug.price * t.number
                result.append(t)
                DB["treatments"].append(t)

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


class Treatment(Object):
    patient: "Patient"
    treatment_id: int
    drug: "Drug"
    number: int
    price: float

    def __init__(
        self, patient: "Patient", treatment_id: int, drug: "Drug", number: int = 0
    ) -> None:
        self.patient = patient
        self.treatment_id = treatment_id
        self.drug = drug
        self.setNumber(number)

    def setNumber(self, number: int):
        self.number = number
        self.price = number * self.drug.price

    def __str__(self) -> str:
        return f"Treatment({self.treatment_id} :: {self.patient}, {self.drug}({self.number}) = {self.price})"


class Drug(Symptomable):
    drug_id: int
    name: str
    price: float

    def __init__(self, drug_id: int, name: str, price: float) -> None:
        super().__init__()
        self.drug_id = drug_id
        self.name = name
        self.price = price

    def __str__(self) -> str:
        return f"Drug({self.drug_id} :: name={self.name}, price={self.price})"

    def addEffect(self, effect: "Effect"):
        self.effects.append(effect)

    def findEffect(self, effect: "Effect") -> "Effect":
        for eff in self.effects:
            if eff.symptom_id == effect.symptom_id:
                return eff
        return None


class Symptom(Object):
    symptom_id: int

    def __init__(self, symptom_id: int, name: str) -> None:
        self.symptom_id = symptom_id
        self.name = name

    def find(symptom_id: int):
        return [
            symptom for symptom in DB["symptoms"] if symptom.symptom_id == symptom_id
        ][0]

    def __str__(self) -> str:
        return f"Symptom({self.symptom_id}, name={self.name})"


class Effect(Relation):
    item: "Symptomable"
    symptom_id: int
    value: float

    def getSymptom(self):
        return [
            symptom
            for symptom in DB["symptoms"]
            if symptom.symptom_id == self.symptom_id
        ][0]

    def getDrugs(self) -> List["Drug"]:
        result = []
        for drug in DB["drugs"]:
            if drug.hasSymptom(self.symptom_id):
                result.append(drug)
        return result

    def __init__(self, item: "Symptomable", symptom_id: int, value: float) -> None:
        self.item = item
        self.symptom_id = symptom_id
        self.value = value

    def __str__(self) -> str:
        symptom = self.getSymptom()
        return f"Effect(symptom={str(symptom)} : value={str(self.value)})"


class Disease(Object):
    disease_id: int

    def __init__(self, disease_id: int, name: str) -> None:
        self.disease_id = disease_id
        self.name = name

    def __str__(self) -> str:
        return f"Disease({self.disease_id} :: name={self.name})"


patient1 = Patient("Alice Smith")
patient2 = Patient("Bob Johnson")
patient3 = Patient("Carol Martinez")
patient4 = Patient("David Lee")
patient5 = Patient("Eva Brown")
patient6 = Patient("Frank Wright")
patient7 = Patient("Grace Green")
patient8 = Patient("Henry Adams")
patient9 = Patient("Ivy White")
patient10 = Patient("Jack Black")

DB["patients"] = [
    patient1,
    patient2,
    patient3,
    patient4,
    patient5,
    patient6,
    patient7,
    patient8,
    patient9,
    patient10,
]

symptom1 = Symptom(1, "Cough")
symptom2 = Symptom(2, "Fever")
symptom3 = Symptom(3, "Headache")
symptom4 = Symptom(4, "Dizziness")
symptom5 = Symptom(5, "Nausea")
symptom6 = Symptom(6, "Rash")
symptom7 = Symptom(7, "Anxiety")
symptom8 = Symptom(8, "Insomnia")
symptom9 = Symptom(9, "Dehydration")
symptom10 = Symptom(10, "Hypertension")

DB["symptoms"] = [
    symptom1,
    symptom2,
    symptom3,
    symptom4,
    symptom5,
    symptom6,
    symptom7,
    symptom8,
    symptom9,
    symptom10,
]


drug1 = Drug(1, "Ibuprofen", 5.99)
drug2 = Drug(2, "Acetaminophen", 4.99)
drug3 = Drug(3, "Amoxicillin", 12.99)
drug4 = Drug(4, "Metformin", 7.99)
drug5 = Drug(5, "Lisinopril", 6.50)
drug6 = Drug(6, "Albuterol", 23.99)
drug7 = Drug(7, "Simvastatin", 8.45)
drug8 = Drug(8, "Aspirin", 3.49)
drug9 = Drug(9, "Cetirizine", 15.00)
drug10 = Drug(10, "Azithromycin", 19.99)
magic = Drug(11, "Magic drug", 0.99)

DB["drugs"] = [
    drug1,
    drug2,
    drug3,
    drug4,
    drug5,
    drug6,
    drug7,
    drug8,
    drug9,
    drug10,
    magic,
]

disease1 = Disease(1, "Flu")
disease2 = Disease(2, "Diabetes")
disease3 = Disease(3, "Hypertension")
disease4 = Disease(4, "Asthma")
disease5 = Disease(5, "Depression")
disease6 = Disease(6, "COVID-19")
disease7 = Disease(7, "Allergies")
disease8 = Disease(8, "Common Cold")
disease9 = Disease(9, "Gastroenteritis")
disease10 = Disease(10, "Heart Disease")

DB["diseases"] = [
    disease1,
    disease2,
    disease3,
    disease4,
    disease5,
    disease6,
    disease7,
    disease8,
    disease9,
    disease10,
]


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


def filterTreatments(
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


drug1.addSymptom(1, -5)
drug2.addSymptom(2, -5)
drug3.addSymptom(3, -5)
drug4.addSymptom(4, -5)
drug5.addSymptom(5, -5)
drug6.addSymptom(6, -5)
drug7.addSymptom(7, -5)
drug8.addSymptom(8, -5)
drug9.addSymptom(9, -5)
drug10.addSymptom(10, -5)

magic.addSymptom(1, -5)
magic.addSymptom(2, -5)
magic.addSymptom(3, -5)
magic.addSymptom(4, -5)
magic.addSymptom(5, -5)
magic.addSymptom(6, -5)
magic.addSymptom(7, -5)
magic.addSymptom(8, -5)
magic.addSymptom(9, -5)
magic.addSymptom(10, -5)


class Consultation:
    patient: "Patient"

    def __init__(self, patient: Patient, symptoms: list):
        self.patient = patient

    def evaluate(self) -> dict[str, Any]:
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

        result = filterTreatments(result)

        print("Here is the List of possible cure:")
        for treatments in result:
            print("Treatment")
            for t in treatments:
                print(f"\t{t}")

        min = get_min(result)

        print("Here is the less expensive treatment:")
        for t in min:
            print(f"\t{t}")

        print(result)

        return {
            "result": result,
            "min": min,
        }


# consultation = Consultation(patient1, [symptom1, symptom2, symptom4])
# consultation.evaluate()
