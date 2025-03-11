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


class GenerateResultsComptabiliteInit(ModelView):
    'Generate Data Compta - Validation'
    __name__ = 'results.compta.init'

class GenerateResultsCompta(Wizard):
    'Generate Data Comptabilite Validation syntheses_commission'
    __name__ = 'results.compta.create'

    start = StateView('results.compta.init',
        'z_validation.view_generate_compta_validation_examen', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Generate Validation', 'generate_compta_examen_validation', 'tryton-ok',
                True),
            ])
    
    generate_compta_examen_validation = StateTransition()

    def transition_generate_compta_examen_validation(self):
        Cotations = Pool().get("syntheses_cotation")
        Commissions = Pool().get("commission")
        Synth_Commissions = Pool().get("syntheses_commission")

        Cotations = Cotations.search([('correct', '=', True)])
        listes_cotations = [cotation.service_cotation for cotation in Cotations]

        Commissions = Commissions.search([])
        Commissions = [commission for commission in Commissions if commission.origin.invoice.reference in listes_cotations]

        list_commissions = []
        dict_commission = {}
        for commission in Commissions:
            dict_commission['service_cotation'] = commission.origin.invoice.reference
            dict_commission['number_invoice'] = commission.origin.invoice.number
            dict_commission['amount'] = commission.amount
            dict_commission['designation'] = commission.origin.product.rec_name
            dict_commission['agent'] = commission.agent.rec_name
            
            a = Synth_Commissions.search([('number_invoice','=', commission.origin.invoice.number), ('service_cotation','=', commission.origin.invoice.reference)])
            if a == []:
                print(a)
                list_commissions.append(dict_commission)
            
            Synth_Commissions.create(list_commissions)

        return 'end'



