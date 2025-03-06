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
    state = fields.Char("Etat", readonly=True)
    observation = fields.Text("Observation", help="Les différentes observations.")
    service_examen = fields.Char('Service Examen', help="Le service en questions")
    correct = fields.Boolean("Correcte", help="Cocher si ceci est bien correct.")

    def __str__(self):
        return self.order

    def retrieve_information(cls, records, trigger):

        today = date.today()
        Syntheses = Pool().get("all_syntheses")
        LabResults = Pool().get("gnuhealth.lab")
        ExpResults = Pool().get("gnuhealth.exp")
        ImgResults = Pool().get("gnuhealth.imaging.test.result")

        order = [('date_analysis', 'ASC')]
        LabResults = LabResults.search(['date_analysis', '=', today], order)
        ExpResults = ExpResults.search(['date_analysis', '=', today], order)
        ImgResults = ImgResults.search(['date', '=', today], order)

        for LabResult in LabResults :
            dur = 0
            patient = LabResult.patient.name.name + " " + LabResult.patient.name.lastname
            if LabResult.done_date :
                dur = LabResult.done_date - LabResult.date_requested
            Syntheses.create([{
                'order' : LabResult.request_order,
                'numero_test' : LabResult.rec_name,
                'actes_examen' : LabResult.test.name,
                'date_emm' : LabResult.date_requested,
                'date_result' : LabResult.done_date,
                'date_eng' : today,
                'duree' : dur,
                'state' : LabResult.state,
                'patient' : patient,
                'service_examen' : 'lab'
            }])
        
        for ExpResult in ExpResults :
            dur = 0
            patient = ExpResult.patient.name.name + " " + ExpResult.patient.name.lastname
            if ExpResult.done_date :
                dur = ExpResult.done_date - ExpResult.date_requested
            Syntheses.create([{
                'order' : ExpResult.request_order,
                'numero_test' : ExpResult.rec_name,
                'actes_examen' : ExpResult.test.name,
                'date_emm' : ExpResult.date_requested,
                'date_result' : ExpResult.done_date,
                'date_eng' : today,
                'duree' : dur,
                'state' : ExpResult.state,
                'patient' : patient,
                'service_examen' : 'exp'
            }])

        for ImgResult in ImgResults :
            dur = 0
            patient = ImgResult.patient.name.name + " " + ImgResult.patient.name.lastname
            if ImgResult.done_date :
                dur = ImgResult.done_date - ImgResult.request_date
            Syntheses.create([{
                'order' : ImgResult.order,
                'numero_test' : ImgResult.number,
                'actes_examen' : ImgResult.requested_test.name,
                'date_emm' : ImgResult.request_date,
                'date_result' : ImgResult.done_date,
                'date_eng' : today,
                'duree' : dur,
                'state' : ImgResult.state,
                'patient' : patient,
                'service_examen' : 'img'
            }])
        if hasattr(Syntheses_Resultats_Examen, 'order'):
            print("ceci a attribut order", cls.date_emm)
    
    def delete_information(cls, records, trigger):

        today = date.today()
        yesterday = today.replace(day=today.day - 1)
        Syntheses = Pool().get("all_syntheses")

        # 🔹 3️⃣ Supprimer les éléments de la veille
        Syntheses_Result = Syntheses.search([('date_eng', '=', yesterday)])
        
        if Syntheses_Result:
            Syntheses.delete(Syntheses_Result)

