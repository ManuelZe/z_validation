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
import re
from trytond.model import ModelView, fields
from trytond.wizard import Wizard, StateTransition, StateView, Button
from trytond.pool import Pool
from datetime import date, datetime, time


class GenerateResultsComptabiliteInit(ModelView):
    'Generate Data Compta - Validation'
    __name__ = 'results.compta.init'

    date_debut = fields.Date("Date de Début")
    date_fin = fields.Date("Date de Fin")

class GenerateResultsCompta(Wizard):
    'Generate Data Comptabilite Validation syntheses_commission'
    __name__ = 'results.compta.create'

    start = StateView('results.compta.init',
        'z_validation.view_generate_compta_validation_examen', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Generate Validation', 'generate_compta_examen_validation', 'tryton-ok',
                True),
            ])
    
    def default_start(self, fields):
        today = date.today()
        default = {
            'date_debut': datetime.combine(today, time.min),
            'date_fin': datetime.combine(today, time.max),
            }
        return default
    
    generate_compta_examen_validation = StateTransition()

    def transition_generate_compta_examen_validation(self):
        Cotations = Pool().get("syntheses_cotation")
        Commissions = Pool().get("commission")
        Synth_Commissions = Pool().get("syntheses_commission")
        start_datetime = datetime.combine(self.start.date_debut, time.min)
        end_datetime = datetime.combine(self.start.date_fin, time.max)

        Invoices = Pool().get("account.invoice")
        Factures = Invoices.search([('invoice_date', '<=', start_datetime), ('invoice_date', '=>', end_datetime)])

        listes_factures = []
        for Facture in Factures:
            if Facture.number not in listes_factures:
                listes_factures.append(Facture.number)

        for Facture in Factures:
            if Facture.reference in listes_factures:
                listes_factures.remove(Facture.reference)
                listes_factures.remove(Facture.number)

        Cotations = Cotations.search([('correct', '=', True)])
        listes_invoices = [cotation.number_invoice for cotation in Cotations]
        listes_examens = [cotation.examen for cotation in Cotations]
        
        for facture in listes_factures:
            if facture.number not in listes_invoices:
                listes_invoices.append[facture.number]
        
        
        Commissions = Commissions.search([])
        Commissions_2 = [commission for commission in Commissions if commission.origin.invoice.number in listes_invoices and re.sub(r"^\[.*?\]\s*", "", commission.origin.product.rec_name) in listes_examens]
        
        for commission in Commissions:
            if commission not in Commissions_2 and commission.origin.invoice.number in listes_invoices:
                Commissions_2.append(commission)

        list_commissions = []
        for commission in Commissions_2:
            dict_commission = {}
            dict_commission['service_cotation'] = commission.origin.invoice.reference
            dict_commission['number_invoice'] = commission.origin.invoice.number
            dict_commission['amount'] = commission.amount
            dict_commission['designation'] = commission.origin.product.rec_name
            dict_commission['agent'] = commission.agent.rec_name

            a = Synth_Commissions.search([('number_invoice','=', commission.origin.invoice.number), ('designation','=', commission.origin.product.rec_name)])
            if a == []:
                list_commissions.append(dict_commission)

        Synth_Commissions.create(list_commissions)

        return 'end'



