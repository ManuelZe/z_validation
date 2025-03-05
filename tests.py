from trytond.model import Workflow, ModelView, ModelSQL, fields
from trytond.pool import Pool

class Syntheses_Resultats_Examen():
    'Synthèses des différents examens journalièrement'
    __name__ = 'all_syntheses'

    order = fields.Numeric("Reste à Payer", readonly=True)
    numero_test = fields.Char("Numéro de test", readonly=True)
    actes_examen = fields.Char("Actes Ou Examens", readonly=True)
    date_emm = fields.DateTime("Date d'Emission", readonly=True)
    date_result = fields.DateTime("Date de Résultat", readonly=True)
    duree = fields.DateTime("Durée", readonly=True)
    patient = fields.Char("Patient", readonly=True)
    observation = fields.Text("Observation", help="Les différentes observations.")
    service_examen = fields.Char('Service Examen', help="Le service en questions")
    correct = fields.Boolean("Correcte", help="Cocher si ceci est bien correct.")

    def __str__(self):
        return self.order

    def retrieve_information(cls, trigger=None):

        if hasattr(Syntheses_Resultats_Examen, 'order'):
            print("ceci a attribut order")
    

undeux = Syntheses_Resultats_Examen()
print(undeux.retrieve_information())
print(dir(undeux))
