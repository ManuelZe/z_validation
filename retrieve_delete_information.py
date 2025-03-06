from trytond.model import Workflow, ModelView, ModelSQL, fields
from trytond.pool import Pool
from datetime import date, timedelta
from trytond.transaction import Transaction
from trytond.config import config
config.update_etc('/home/gnuhealth/gnuhealth/tryton/server/config/trytond.conf')

def retrive_information():

    today = date.today()
    print(Pool.database_list)

    transaction=Transaction()
    with transaction.start(database_name='pdmd_sante', user=1):
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

        yesterday = today - timedelta(days=1)
        Syntheses = Pool().get("all_syntheses")

        # 🔹 3️⃣ Supprimer les éléments de la veille
        Syntheses_Result = Syntheses.search([('date_eng', '=', yesterday)])

        if Syntheses_Result:
            Syntheses.delete(Syntheses_Result)

        Transaction().commit()

if __name__ == "__main__":
    retrive_information()