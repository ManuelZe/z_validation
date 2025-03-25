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
import re

class ActualiseCommissionInit(ModelSQL,ModelView):
    'Actualize Commission - Init'
    __name__ = 'actualize.commission.init'


class ActualiseCommission(Wizard):
    'Actualize Commission'
    __name__ = 'actualize.commission'

    start = StateView('actualize.commission.init',
        'z_validation.view_actualize_commission_init', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Actualiser COMMISSIONS', 'actualize_commission', 'tryton-ok',
                True),
            ])
    actualize_commission = StateTransition()

    def transition_actualize_commission(self):
        Commissions = Pool().get("commission")
        Synth_Commissions = Pool().get("syntheses_commission")

        Comptas = Synth_Commissions.search([('correct', '=', True)])

        for Compta in Comptas:
            Commissions_Search = Commissions.search([('origin.invoice.reference', '=', Compta.number_invoice, 'account.invoice.line'), 
                                                     ('origin.product.name', '=', re.sub(r"^\[.*?\]\s*", "", Compta.designation), 'account.invoice.line')])
            for commission in Commissions_Search :
                if commission.is_validate != True :
                    commission.is_validate = True
                    Commissions_Search.save([commission])

        return 'end'


