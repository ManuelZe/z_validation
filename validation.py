from trytond.model import Workflow, ModelView, ModelSQL, fields
from trytond.pool import Pool
from datetime import date

class Syntheses_Resultats_Examen(ModelSQL, ModelView):
    'Synthèses des différents examens journalièrement'
    __name__ = 'all_syntheses'

    order = fields.Numeric("Ordre", readonly=True)
    numero_test = fields.Char("Numéro de test", readonly=True)
    actes_examen = fields.Char("Actes Ou Examens", readonly=True)
    date_emm = fields.DateTime("Date d'Emission", readonly=True)
    date_eng = fields.DateTime("Date d'Enregistrement", readonly=True)
    date_result = fields.DateTime("Date de Résultat", readonly=True)
    duree = fields.DateTime("Durée", readonly=True)
    patient = fields.Char("Patient", readonly=True)
    service_cotation = fields.Char("Service de Cotation", readonly=True)
    state = fields.Char("Etat", readonly=True)
    observation = fields.Text("Observation", help="Les différentes observations.")
    service_examen = fields.Char('Service Examen', help="Le service en questions")
    correct = fields.Boolean("Correcte", help="Cocher si ceci est bien correct.")



class Syntheses_Pivot(ModelSQL, ModelView):
    'Synthèses des différents Service de Cotation'
    __name__ = 'syntheses_cotation'

    service_cotation = fields.Char("Service de COtation", readonly=True)
    date_service = fields.Date("Date du Service de Cotation", readonly=True)
    patient = fields.Char("Patient", readonly=True)
    etat = fields.Char("Etat du Service", readonly=True)
    prescripteur = fields.Char("Prescripteur", readonly=True)
    date_invoice = fields.Char("Date de la Facture", readonly=True)
    number_invoice = fields.Char("Numero de Facture", readonly=True)
    correct = fields.Boolean("Correcte", help="Cocher si ceci est bien correct.")