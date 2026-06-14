# ------------------------------------------------------------
# Caso de prueba inyeccion SQL StockHistory
#
# Requerimiento funcional
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
from django.urls import reverse
from stock.models import StockHistory, Category
from django.utils import timezone
from django.core.exceptions import ValidationError


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
    return category

# ============================================================
# PRUEBAS DE SQL INJECTION
# ============================================================

class TestSQLInjectionHistorial:
    
    @pytest.mark.parametrize("payload", [
        # Payloads básicos
        "' OR '1'='1",
        "' OR 1=1 --",
        "1' OR '1'='1",
        
        # Payloads de eliminación
        "'; DROP TABLE stock_stockhistory; --",
        "'; DELETE FROM stock_stockhistory WHERE '1'='1",
        
        # Payloads de modificación
        "'; UPDATE stock_stockhistory SET quantity=9999 WHERE item_name='Laptop' --",
        
        # Payloads de tiempo
        "' AND SLEEP(5) --",
        "' OR pg_sleep(5) --",
        
        # Payloads comentados
        "'/**/OR/**/1=1--",
        "1' AND '1' LIKE '1",
        
    ])
    # Test en el campo de items
    def test_sql_injection_item_name(self, usuario_base, setup_history, payload):
        """Prueba SQL injection en el campo item_name"""

        response = usuario_base.post('/view_history', {
            'item_name': payload,
            'start_date': '',
            'end_date': '',
            'category': '',
            'export_to_CSV': False
        })
        
        assert response.status_code != 500, f"Error 500 con payload: {payload}"
        assert response.status_code in [200, 302, 400]
        
    # Test en el campo de fechaInicio    
    @pytest.mark.parametrize("payload", [
        "' OR '1'='1",
        "2024-01-01 00:00:00' AND SLEEP(5) --",
        "2024-01-01 00:00:00'; DROP TABLE stock_stockhistory; --",
        "' UNION SELECT 1,2,3 --",
    ])
    def test_sql_injection_start_date(self, usuario_base, setup_history, payload):
        """Prueba SQL injection en el campo start_date"""

        response = usuario_base.post('/view_history', {
            'item_name': '',
            'start_date': payload,
            'end_date': '2024-12-31 00:00:00',
            'category': '',
            'export_to_CSV': False
        })
        assert response.status_code != 500
        assert response.status_code in [200, 302, 400]
        
    # Test en el campo de fechaFin    
    @pytest.mark.parametrize("payload", [
        "' OR '1'='1",
        "' UNION SELECT 1,2,3 --",
    ])
    def test_sql_injection_end_date(self, usuario_base, setup_history, payload):
        """Prueba SQL injection en el campo end_date"""

        response = usuario_base.post('/view_history', {
            'item_name': '',
            'start_date': '2024-01-01 00:00:00',
            'end_date': payload,
            'category': '',
            'export_to_CSV': False
        })
        
        assert response.status_code != 500
        assert response.status_code in [200, 302, 400]

    # Test en el campo de categoria
    @pytest.mark.parametrize("payload", [
        "' OR '1'='1",
        "1; DROP TABLE stock_category; --",
        "' UNION SELECT 1,2,3 --",
    ])
    
    def test_sql_injection_category(self, usuario_base, setup_history, payload):
        """Prueba SQL injection en el campo category"""

        response = usuario_base.post('/view_history', {
            'item_name': '',
            'start_date': '',
            'end_date': '',
            'category': payload,
            'export_to_CSV': False
        })
        
        assert response.status_code != 500
        assert response.status_code in [200, 302, 400]
        
    # Test en multiples campos
    def test_multiple_filters_sql_injection(self, usuario_base, setup_history):
        """Prueba SQL injection con múltiples campos a la vez"""
        
        response = usuario_base.post('/view_history', {
            'item_name': "' OR '1'='1",
            'start_date': "2024-01-01 00:00:00' AND SLEEP(5) --",
            'end_date': "' OR '1'='1",
            'category': "1; DROP TABLE stock_category; --",
            'export_to_CSV': False
        })
        
        assert response.status_code != 500
        assert response.status_code in [200, 302, 400]
        
        # Verificar que los datos originales existen
        assert StockHistory.objects.filter(item_name='Laptop').exists()






