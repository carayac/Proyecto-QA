# Para correr estas pruebas correr instalar pytest
# pip install pytest
# Luego correr esto en la terminal
# pytest tests_seguridad/unitarios_seguridad.py -v


from django.test import TestCase

import pytest
from django.test import Client #para crear cliente en django
from django.contrib.auth.models import User #para crear user en django
from django.contrib.auth import authenticate #para llamar a la funcion authenticate, 
                                            # que es la que vamos a probar en django

# ---------------------------------------------
# Pruebas unitarias RNF-02: Seguridad
# ---------------------------------------------

@pytest.fixture
def usuario_base(db):
    # Se crea el usuario de prueba
    return User.objects.create_user(
        username='hp',
        password='dev-password-local'
    )

@pytest.fixture
def cliente():
    # Se crea un cliente de django
    return Client()


# # --- CP-041 Login con SQL Injection
# @pytest.mark.parametrize(
#     "username,password",
#     [
#         ("' OR 1=1 --", "' OR 1=1 --"),
#         ("hp'; DROP TABLE auth_user; --", "test"),
#         ("' UNION SELECT * FROM auth_user --", "test"),
#     ]
# )


# def test_login_sql_injection(usuario_base, username, password):
#     user = authenticate(username=username, password=password)

#     # La autenticación debe fallar
#     assert user is None


# ---------------------------------------------
# Pruebas de integración RNF-02: Seguridad
# ---------------------------------------------

# --- CP-042 Verificación de token de sesión
def test_generacion_cookie_sesion(usuario_base, cliente):

    # Se realiza el login
    login_exitoso = cliente.login(
        username='hp',
        password='dev-password-local'
    )

    # El login debe ser exitoso
    assert login_exitoso is True

    # Debe generarse la cookie de sesión
    assert 'sessionid' in cliente.cookies

    # La cookie no debe estar vacía
    assert cliente.cookies['sessionid'].value != ''