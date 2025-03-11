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
from trytond.model import ModelView
from trytond.wizard import Wizard, StateTransition, StateView, Button
from trytond.transaction import Transaction
from trytond.pool import Pool


class GenerateResultsCotationInit(ModelView):
    'Generate Data Cotation - Validation'
    __name__ = 'results.cotation.init'


class GenerateResultsCotation(Wizard):
    'Generate Data Cotation Validation syntheses_cotation'
    __name__ = 'results.cotation.create'

    start = StateView('results.cotation.init',
        'z_validation.view_generate_cotation_validation_examen', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Generate Validation', 'generate_cotation_examen_validation', 'tryton-ok',
                True),
            ])
    generate_cotation_examen_validation = StateTransition()

    def transition_generate_cotation_examen_validation(self):
        Examens = Pool().get("all_syntheses")
        Cotations = Pool().get('syntheses_cotation')
        Services = Pool().get("gnuhealth.health_service")
        Invoices = Pool().get("account.invoice")

        Examens = Examens.search([('correct', '=', True)])
        liste_cotations = [examen.service_cotation for examen in Examens]
        Services_Invoices = Invoices.search([('reference', 'in', liste_cotations), ('state', 'in', ['paid', 'posted'])])

        # Voici le parcours utilisé pour avoir ses données
        # Nous prenons une liste des services de cotation des différents Examens
        # Corrects précédemment Obtenus.
        # Ensuite On récupère les factures dont la référence(service de cotation)
        # est à l'intérieur de la liste des service de cotations.
        # Aprs on boucle les factures pour remplir le syntheses_cotation naturellement

        cotations = []
        elt_cotation = {}
        
        for invoice in Services_Invoices:
            service = Services.search([('name', '=', invoice.reference)])
            elt_cotation['service_cotation'] = service[0].name
            elt_cotation['date_service'] = service[0].service_date
            elt_cotation['patient'] = service[0].patient.name.name + " " + service[0].patient.name.lastname
            elt_cotation['etat'] = service[0].state
            elt_cotation['prescripteur'] = service[0].requestor.name.name + " " + service[0].requestor.name.lastname
            elt_cotation['date_invoice'] = invoice.invoice_date
            elt_cotation['number_invoice'] = invoice.number

            if Cotations.search([('number_invoice','=', invoice.number)]) == []:
                cotations.append(elt_cotation)

        Cotations.create(cotations)
        
        return 'end'
    


        