# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.pool import Pool
from . import validation
from .wizard import generate_result_reports
from .wizard import generate_cotation

__all__ = ['register']


def register():
    Pool.register(
        validation.Syntheses_Resultats_Examen,
        generate_result_reports.GenerateResultsExamenInit,
        generate_cotation.GenerateResultsCotationInit,
        module='z_validation', type_='model')
    Pool.register(
        generate_result_reports.GenerateResultsExamen,
        generate_cotation.GenerateResultsCotation,
        module='z_validation', type_='wizard')
    Pool.register(
        module='z_validation', type_='report')
