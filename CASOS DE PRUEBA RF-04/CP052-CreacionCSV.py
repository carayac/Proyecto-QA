# ------------------------------------------------------------
# Caso de prueba unitaria sobre CSV en HistoryStock
#
# Prueba integracion
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

from django.test import Client
from django.contrib.auth.models import User
from stock.models import StockHistory, Category
from django.utils import timezone


# Fixture para crear datos de prueba

@pytest.fixture
def usuario_base():
    user, created = User.objects.get_or_create(
        username='hp',
        defaults={'password': 'dev-password-local'}
    )
    if created:
        user.set_password('dev-password-local')
        user.save()
    
    client = Client()
    client.login(username='hp', password='dev-password-local')
    return client


@pytest.fixture
def setup_history():
    category, _ = Category.objects.get_or_create(group='Electronics')   
    StockHistory.objects.create(
        category=category,
        item_name='Laptop',
        quantity=10,
        last_updated=timezone.now()
    )


    # ============================================================
    # PRUEBAS DE EXPORTACIÓN CSV
    # ============================================================
@pytest.mark.django_db
class TestCSVCreation:
    
    def test_csv_export_headers_correct(self, usuario_base, setup_history):
        """Encabezados del CSV deben ser correctos"""
        response = usuario_base.post('/view_history', {
            'item_name': 'Laptop',
            'start_date': '2024-01-01 00:00:00',
            'end_date': '2027-01-01 00:00:00',
            'category': '',            
            'export_to_CSV': True
        })
        
        content = response.content.decode('utf-8')
        content = content.replace('\r', '')
        headers = content.split('\n')[0].split(',')
    
        expected_headers = [
            'CATEGORY', 'ITEM NAME', 'QUANTITY', 'ISSUE QUANTITY',
            'RECEIVE QUANTITY', 'RECEIVE BY', 'ISSUE BY', 'LAST UPDATED'
        ]
        
        assert headers == expected_headers



    def test_csv_export_empty_result(self, usuario_base, setup_history):
        """Exportar CSV sin resultados - solo encabezados"""
        response = usuario_base.post('/view_history', {
            'item_name': 'NOEXISTE',
            'start_date': '2024-01-01 00:00:00',
            'end_date': '2027-01-01 00:00:00',
            'category': '',
            'export_to_CSV': True
        })
        
        content = response.content.decode('utf-8')
        lines = content.strip().split('\n')
        
        # Solo encabezados (1 línea)
        assert len(lines) == 1
        assert 'CATEGORY' in lines[0]
    










