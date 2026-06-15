# ------------------------------------------------------------
# Caso de prueba logueo en HistoryStock
#
# Requerimiento seguridad
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
def sin_login():
    return Client()
    

@pytest.fixture
def con_login():
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
# PRUEBAS DE ACCESO SIN LOGIN
# ============================================================

@pytest.mark.django_db
class TestAccessViewHistory:
    
    # ============================================================
    # GET /view_history
    # ============================================================
    
    def test_UNauthenticated_view_history(self, sin_login):
        """Usuario NO autenticado NO puede ver el historial"""
        response = sin_login.get('/view_history')
        
        # Debe redirigir al login (302)
        assert response.status_code == 302
        assert '/accounts/login/' in response.url
    
    def test_authenticated_view_history(self, con_login, setup_history):
        """Usuario autenticado SI puede ver el historial"""
        response = con_login.get('/view_history')
        
        assert response.status_code == 200
    
   
    # ============================================================
    # POST /view_history (con filtros)
    # ============================================================
    
    def test_UNauthenticated_post_filters(self, sin_login):
        """Usuario NO autenticado NO puede aplicar filtros"""
        response = sin_login.post('/view_history', {
            'item_name': 'Laptop',
            'start_date': '',
            'end_date': '',
            'category': '',
            'export_to_CSV': False
        })
        
        assert response.status_code == 302
        assert '/accounts/login/' in response.url
    
    def test_authenticated_post_filters(self, con_login, setup_history):
        """Usuario autenticado SÍ puede aplicar filtros"""
        response = con_login.post('/view_history', {
            'item_name': 'Laptop',
            'start_date': '2024-01-01 00:00:00',
            'end_date': '2027-01-01 00:00:00',
            'category': '',
            'export_to_CSV': False
        })
        
        assert response.status_code == 200














    
