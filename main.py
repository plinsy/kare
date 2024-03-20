class Disease:
    values: list["Disease"] = []
    disease_id: int
    name: str

    def find(disease_id: int):
        return [
            disease for disease in Disease.values if disease.disease_id == disease_id
        ][0]

    def __init__(self, disease_id, name) -> None:
        self.disease_id = disease_id
        self.name = name

    def __str__(self) -> str:
        return "Disease[" + str(self.disease_id) + ", " + self.name + "]"


class Affect:
    pass


class Drug:
    values: list["Drug"] = []
    drug_id: int
    name: str
    price: float
    effects: list["Effect"] = []

    def find(drug_id: int):
        return [drug for drug in Drug.values if drug.drug_id == drug_id][0]

    def __init__(self, drug_id, name, price=0.0) -> None:
        self.drug_id = drug_id
        self.name = name
        self.price = price

    def __str__(self) -> str:
        return "Drug[" + str(self.drug_id) + ", " + self.name + "]"


class Effect:
    values: list["Effect"] = []
    disease_id: int
    drug_id: int
    value: int

    def find(drug_id: int, disease_id: int) -> "Effect":
        results = [
            effect
            for effect in Effect.values
            if effect.drug_id == drug_id and effect.disease_id == disease_id
        ]
        if results.__len__() == 0:
            return None
        return results[0]

    def __init__(self, drug_id, disease_id, value) -> None:
        self.drug_id = drug_id
        self.disease_id = disease_id
        self.value = value

    def __str__(self) -> str:
        return (
            "Effect["
            + self.drug_id.__str__()
            + " - "
            + self.disease_id.__str__()
            + " : "
            + self.value.__str__()
            + "]"
        )


class Symptom:
    disease_id: int
    value: int

    def __init__(self, disease_id, value) -> None:
        self.disease_id = disease_id
        self.value = value

    def __str__(self) -> str:
        return "Symptom[" + self.disease_id + " : " + self.value + "]"


class Treatment:
    values: list["Treatment"] = []
    disease_id: int
    drug_id: int
    number: int
    price: float

    def __init__(self, drug_id, disease_id, price, number=0) -> None:
        self.disease_id = disease_id
        self.drug_id = drug_id
        self.price = price
        self.number = number

    def __str__(self) -> str:
        disease = Disease.find(self.disease_id)
        drug = Drug.find(self.drug_id)
        return (
            "Treatment["
            + str(disease)
            + " => "
            + "("
            + self.number.__str__()
            + ") * "
            + str(drug)
            + " : "
            + self.price.__str__()
            + "]"
        )


class Diagnostic:
    def get_treatments_for(self, symptom: Symptom) -> list[Treatment]:
        result = []
        for drug in Drug.values:
            t = Treatment(disease_id=symptom.disease_id, drug_id=drug.drug_id, price=0)
            effect = Effect.find(drug.drug_id, symptom.disease_id)
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
            if effect != None and effect.value < 0 and symptom.value > 0:
                t.number = round(-(symptom.value) / effect.value)
                t.price += drug.price * t.number
                result.append(t)
                Treatment.values.append(t)
            else:
                pass

        return result

    def get_all_treatments_for(self, symptoms: list[Symptom]) -> list[list[Treatment]]:
        result = []
        for symptom in symptoms:
            sub_treatments = self.get_treatments_for(symptom)
            if len(sub_treatments) > 0:
                result.append(sub_treatments)
        return result


d1 = Disease(disease_id=1, name="Diarhée")
d2 = Disease(disease_id=2, name="Nausée")
d3 = Disease(disease_id=3, name="Maux de tête")

Disease.values = [d1, d2, d3]

g1 = Drug(drug_id=1, name="A", price=50.00)
g2 = Drug(drug_id=2, name="B", price=20.00)
g3 = Drug(drug_id=3, name="C", price=75.00)
g4 = Drug(drug_id=4, name="D", price=25.00)

Drug.values = [g1, g2, g3, g4]

e1 = Effect(drug_id=1, disease_id=1, value=-1)
e2 = Effect(drug_id=1, disease_id=2, value=-2)
e3 = Effect(drug_id=1, disease_id=3, value=-3)

e4 = Effect(drug_id=2, disease_id=1, value=-2)
e5 = Effect(drug_id=2, disease_id=2, value=-3)
e6 = Effect(drug_id=2, disease_id=3, value=-4)

e7 = Effect(drug_id=3, disease_id=1, value=-3)
e8 = Effect(drug_id=3, disease_id=2, value=-4)
e9 = Effect(drug_id=3, disease_id=3, value=0)

Effect.values = [e1, e2, e3, e4, e5, e6, e7, e8, e9]

s1 = Symptom(disease_id=1, value=5)
s2 = Symptom(disease_id=2, value=15)
s3 = Symptom(disease_id=3, value=0)

illness = [s1, s2, s3]

diag1 = Diagnostic()
medecins = diag1.get_all_treatments_for(illness)

# diag2 = Diagnostic()
# t1 = diag2.get_treatments_for(s1)

for treatments in medecins:
    print("\t")
    for t in treatments:
        print(t)


def product(*args):
    if not args:
        return [()]
    result = []
    for prod in args[0]:
        for rest in product(*args[1:]):
            result.append((prod,) + rest)
    return result


results: list[list[Treatment]] = product(*medecins)

for treatments in results:
    print("\t")
    for t in treatments:
        print(t)
