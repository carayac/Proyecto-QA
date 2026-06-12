# Para correr estas pruebas, primero instalar playwright y pytest
# pip install pytest
# pip install playwright
# playwright install
# Luego levantar el servidor
# python manage.py runserver
# luego en una terminal diferente
# pytest tests_seguridad/funcionales_seguridad.py --headed -v


import pytest
from playwright.sync_api import Page, expect
from django.contrib.auth.models import User

@pytest.fixture
def usuario_base(db):
    #crear usuario de django
    User.objects.create_user(
        username="hp",
        password="dev-password-local"
    )

# ---------------------------------------------
# Pruebas funcionales RNF-02: Seguridad
# --------------------------------------------

# --- CP-045 - Bloqueo de acceso tras muchos intentos fallidos
def test_bloqueo_por_intentos_fallidos(page: Page):

    page.goto("http://127.0.0.1:8000/accounts/login/")

    # Realizar 5 intentos fallidos consecutivos
    for _ in range(5):

        page.get_by_label("Username").fill("hp")
        page.get_by_label("Password").fill("incorrecto")

        page.get_by_role("button", name="Login").click()

        expect(page).to_have_url(
            "http://127.0.0.1:8000/accounts/login/"
        )

    # Sexto intento: la cuenta debería estar bloqueada
    page.get_by_label("Username").fill("hp")
    page.get_by_label("Password").fill("dev-password-local")

    page.get_by_role("button", name="Login").click()

    # Verificar mensaje de bloqueo
    expect(page).to_have_url(
        "http://127.0.0.1:8000/accounts/login/"
    )