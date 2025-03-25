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

        # 1️⃣ Récupérer tous les examens corrects en une seule requête
        Examens = Examens.search([('correct', '=', True)])

        # 2️⃣ Construire une liste des références de cotation
        liste_cotations = [examen.service_cotation for examen in Examens]
        print("La liste des cotations ----- ", len(liste_cotations))

        # 3️⃣ Récupérer toutes les factures associées en une seule requête
        Services_Invoices = Invoices.search([
            ('reference', 'in', liste_cotations),
            ('state', 'in', ['paid', 'posted'])
        ])
        print("Le service Invoice -- ", len(Services_Invoices))

        # 4️⃣ Récupérer tous les services en une seule requête (évite `search` répétitif)
        service_map = {service.name: service for service in Services.search([('name', 'in', liste_cotations)])}

        # 5️⃣ Préparer une liste pour batch-create
        cotations = []

        # 6️⃣ Boucle optimisée
        for invoice in Services_Invoices:
            service = service_map.get(invoice.reference)  # Évite un search inutile
            if not service:
                continue  # Skip si le service n'est pas trouvé

            for exam in Examens:
                elt_cotation = {
                    'service_cotation': service.name,
                    'date_service': service.service_date,
                    'patient': f"{service.patient.name.name} {service.patient.name.lastname}",
                    'etat': service.state,
                    'prescripteur': f"{service.requestor.name.name} {service.requestor.name.lastname}",
                    'date_invoice': invoice.invoice_date,
                    'number_invoice': invoice.number,
                    'examen': exam.actes_examen,
                }

                # 7️⃣ Vérifier l'existence en lot pour éviter des `search` dans la boucle
                if not Cotations.search([
                    ('number_invoice', '=', invoice.number),
                    ('examen', '=', exam.actes_examen)
                ]):
                    cotations.append(elt_cotation)

        # 8️⃣ Créer les cotations en lot (au lieu de plusieurs appels `create`)
        if cotations:
            Cotations.create(cotations)

        
        return 'end'
    


        