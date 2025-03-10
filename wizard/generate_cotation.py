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
        
        Examens = Examens.search([('correct', '=', True)])

        cotations = []

        