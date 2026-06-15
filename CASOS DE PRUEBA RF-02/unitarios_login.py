# Para correr estas pruebas correr instalar pytest
# pip install pytest
# Luego correr esto en la terminal
# pytest tests_login/unitarios_login.py -v
# o para correr un test individual
# pytest tests_login/funcionales_login.py::test_login_valido -v

from django.test import TestCase

import pytest
from django.test import Client #para crear cliente en django
from django.contrib.auth.models import User #para crear user en django
from django.contrib.auth import authenticate #para llamar a la funcion authenticate, 
                                            # que es la que vamos a probar en django


# ---------------------------------------------
# Pruebas unitarias RF-02: Autenticación
# --------------------------------------------

@pytest.fixture
def usuario_base(db):
    #Se crea el usuario de prueba
    return User.objects.create_user(
        username='hp',
        password='dev-password-local'
    )

@pytest.fixture
def cliente():
    #Se crea un cliente de django
    return Client()


# --- CP-021 Login con credenciales válidas
def test_login_valido(usuario_base):
    user = authenticate(username='hp', password='dev-password-local')
    assert user is not None
    assert user.is_authenticated


# --- CP-022 Login con contraseña incorrecta
def test_contrasena_incorrecta(usuario_base):
    user = authenticate(username='hp', password='incorrecto')
    assert user is None
