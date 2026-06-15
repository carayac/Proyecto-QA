# ------------------------------------------------------------
# Caso de prueba unitaria sobre el formulario StockHistorySearchForm
#
# Prueba unitaria
# Utilizando pytest
# ------------------------------------------------------------

import pytest
import sys
import os
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # Proyecto-QA
sys.path.append(str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stockmgtr.settings")
django.setup()

from stock.form import StockHistorySearchForm
from django.core.exceptions import ValidationError
from django import forms


@pytest.mark.unit
class TestStockHistorySearchForm:

    def test_form_reject_unknown_field(self):
        """Campo que no existe debe ser rechazado"""
        form = StockHistorySearchForm(data={
            'campo_inexistente': 'valor'
        })
        assert form.is_valid()
    
    def test_form_reject_invalid_date_format(self):
        """Fechas inválidas DEBERÍAN ser rechazadas"""
        form = StockHistorySearchForm(data={
            'start_date': 'esto no es una fecha',
            'end_date': 'tampoco es fecha'
        })
        assert not form.is_valid()

    def test_form_reject_non_boolean_export_to_csv(self):
        """Valor no booleano en export_to_CSV debe ser rechazado o manejado"""
        form = StockHistorySearchForm(data={
            'export_to_CSV': 'no soy booleano'
        })
        assert form.is_valid()
        assert form.cleaned_data.get('export_to_CSV') is True



        
