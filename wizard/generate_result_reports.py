# -*- coding: utf-8 -*-
##############################################################################
#
#    GNU Health: The Free Health and Hospital Information System
#    Copyright (C) 2008-2022 Luis Falcon <lfalcon@gnusolidario.org>
#    Copyright (C) 2011-2022 GNU Solidario <health@gnusolidario.org>
#
#
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from datetime import date, timedelta, datetime, time
from trytond.model import ModelView, ModelSQL, fields
from trytond.wizard import Wizard, StateTransition, StateView, Button
from trytond.transaction import Transaction
from trytond.pool import Pool


class GenerateResultsExamenInit(ModelSQL,ModelView):
    'Generate Data Exam - Validation'
    __name__ = 'results.examen.init'

    date_debut = fields.Date("Date de Début")
    date_fin = fields.Date("Date de Fin")


class GenerateResultsExamen(Wizard):
    'Generate Data Exam Validation All_syntheses'
    __name__ = 'results.examen.create'

    start = StateView('results.examen.init',
        'z_validation.view_generate_results_validation_examen', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Generate Validation', 'generate_results_examen_validation', 'tryton-ok',
                True),
            ])

    def default_start(self, fields):
        today = date.today()
        default = {
            'date_debut': datetime.combine(today, time.min),
            'date_fin': datetime.combine(today, time.max),
            }
        return default
    
    generate_results_examen_validation = StateTransition()

    def transition_generate_results_examen_validation(self):

        today = date.today()
        pool = Pool()
        Syntheses = Pool().get("all_syntheses")
        LabResults = Pool().get("gnuhealth.lab")
        LabRequests = Pool().get("gnuhealth.patient.lab.test")
        ExpResults = Pool().get("gnuhealth.exp")
        ExpRequests = Pool().get("gnuhealth.patient.exp.test")
        ImgResults = Pool().get("gnuhealth.imaging.test.result")
        ImgRequests = Pool().get("gnuhealth.imaging.test.request")

        start_datetime = datetime.combine(self.start.date_debut, time.min)
        end_datetime = datetime.combine(self.start.date_fin, time.max)
        LabResults = LabResults.search([('date_analysis', '>=', start_datetime),
                                        ('date_analysis', '<=', end_datetime)])
        ExpResults = ExpResults.search([('date_analysis', '>=', start_datetime),
                                        ('date_analysis', '<=', end_datetime)])
        ImgResults = ImgResults.search([('date', '>=', start_datetime),
                                        ('date', '<=', end_datetime)])

        for LabResult in LabResults :
            data = {}
            dur = 0
            patient = LabResult.patient.name.name + " " + LabResult.patient.name.lastname
            Service = LabRequests.search([('request', '=', LabResult.request_order)], limit=1)
            if LabResult.done_date :
                dur = LabResult.done_date - LabResult.date_requested
            else :
                dur = timedelta(hours=0, minutes=0, seconds=0)

            tests_id = 'lab' + str(LabResult.id)
            data = {
                'order' : LabResult.request_order,
                'numero_test' : LabResult.rec_name,
                'actes_examen' : LabResult.test.name,
                'date_emm' : LabResult.date_requested,
                'date_result' : LabResult.done_date,
                'date_eng' : datetime.now(),
                'state' : LabResult.state,
                'patient' : patient,
                'tests_id' : tests_id,
                'service_cotation' : Service[0].service.name,
                'service_examen' : 'lab'
            }

            if Syntheses.search([('tests_id','=', tests_id)]) == []:
                Syntheses.create([data])
            else :
                synth = Syntheses.search([('tests_id','=', tests_id)])
                synth[0].state = LabResult.state
                Syntheses.save([synth])

        for ExpResult in ExpResults :
            data = {}
            dur = 0
            patient = ExpResult.patient.name.name + " " + ExpResult.patient.name.lastname
            Service = ExpRequests.search([('request', '=', ExpResult.request_order)], limit=1)
            if ExpResult.done_date :
                dur = ExpResult.done_date - ExpResult.date_requested
            
            tests_id = 'exp' + str(ExpResult.id)
            data = {
                'order' : ExpResult.request_order,
                'numero_test' : ExpResult.rec_name,
                'actes_examen' : ExpResult.test.name,
                'date_emm' : ExpResult.date_requested,
                'date_result' : ExpResult.done_date,
                'date_eng' : datetime.now(),
                'state' : ExpResult.state,
                'patient' : patient,
                'tests_id' : tests_id,
                'service_cotation' : Service[0].service.name,
                'service_examen' : 'exp'
            }

            if Syntheses.search([('tests_id','=', tests_id)]) == []:
                Syntheses.create([data])
            else :
                synth = Syntheses.search([('tests_id','=', tests_id)])
                synth[0].state = ExpResult.state
                Syntheses.save([synth])

        for ImgResult in ImgResults :
            dur = 0
            patient = ImgResult.patient.name.name + " " + ImgResult.patient.name.lastname
            Service = ImgRequests.search([('request', '=', ImgResult.order)], limit=1)
            if ImgResult.done_date :
                dur = ImgResult.done_date - ImgResult.request_date
            tests_id = 'img' + str(ImgResult.number)
            data = {
                'order' : ImgResult.order,
                'numero_test' : ImgResult.number,
                'actes_examen' : ImgResult.requested_test.name,
                'date_emm' : ImgResult.request_date,
                'date_result' : ImgResult.done_date,
                'date_eng' : datetime.now(),
                'state' : ImgResult.state,
                'patient' : patient,
                'tests_id' : tests_id,
                'service_cotation' : Service[0].service.name,
                'service_examen' : 'img'
            }
            if Syntheses.search([('tests_id','=', tests_id)]) == []:
                Syntheses.create([data])
            else :
                synth = Syntheses.search([('tests_id','=', tests_id)])
                synth[0].state = ImgResult.state
                Syntheses.save([synth])

        return 'end'
