# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.pool import Pool
from . import validation
from .wizard import generate_result_reports
from .wizard import generate_cotation
from .wizard import generate_compta

__all__ = ['register']


def register():
    Pool.register(
        validation.Syntheses_Resultats_Examen,
        validation.Syntheses_Pivot,
        validation.Syntheses_Commission,
        generate_result_reports.GenerateResultsExamenInit,
        generate_cotation.GenerateResultsCotationInit,
        generate_compta.GenerateResultsComptabiliteInit,
        module='z_validation', type_='model')
    Pool.register(
        generate_result_reports.GenerateResultsExamen,
        generate_cotation.GenerateResultsCotation,
        generate_compta.GenerateResultsCompta,
        module='z_validation', type_='wizard')
    Pool.register(
        module='z_validation', type_='report')
