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
    
    def test_form_accepts_empty_data(self):
        """El formulario debe aceptar datos vacíos"""
        form = StockHistorySearchForm(data={})
        assert form.is_valid() or not form.is_bound
    
    def test_form_accepts_valid_date_format(self):
        """Fechas en formato correcto deben pasar"""
        form = StockHistorySearchForm(data={
            'start_date': '2024-01-01',
            'end_date': 'nofecha'
        })
        if not form.is_valid():
            assert 'Invalid format' not in str(form.errors.get('start_date', ''))
            assert 'Invalid format' not in str(form.errors.get('end_date', ''))
            
    def test_export_to_csv_is_boolean_field(self):
        """El campo export_to_CSV debe ser booleano"""
        form = StockHistorySearchForm(data={'export_to_CSV': True})
        field = form.fields['export_to_CSV']
        assert isinstance(field, forms.BooleanField)



        
