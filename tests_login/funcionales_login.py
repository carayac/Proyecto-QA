# Para correr estas pruebas, primero instalar playwright y pytest
# pip install pytest
# pip install playwright
# playwright install
# Luego levantar el servidor
# python manage.py runserver
# luego en una terminal diferente
# pytest tests_login/funcionales_login.py --headed -v
# o para correr un test individual
# pytest tests_login/funcionales_login.py::test_login_correcto --headed -v


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
# Pruebas funcionales RF-02: Autenticación
# --------------------------------------------

# # --- CP-026 - Login correcto
def test_login_correcto(page: Page):

    page.goto("http://127.0.0.1:8000/accounts/login/")

    page.get_by_label("Username").fill("hp")
    page.get_by_label("Password").fill("dev-password-local")

    page.get_by_role("button", name="Login").click()

    expect(page).to_have_url(
        "http://127.0.0.1:8000/"
    )

# --- CP-027 - Campo usuario vacío
def test_login_usuario_vacio(page: Page):

    page.goto("http://127.0.0.1:8000/accounts/login/")

    page.get_by_label("Username").fill("")
    page.get_by_label("Password").fill("dev-password-local")

    page.get_by_role("button", name="Login").click()

    expect(page).to_have_url(
    "http://127.0.0.1:8000/accounts/login/"
)

# --- CP-028 - Campo contraseña vacío
def test_login_contrasena_vacia(page: Page):

    page.goto("http://127.0.0.1:8000/accounts/login/")

    page.get_by_label("Username").fill("hp")
    page.get_by_label("Password").fill("")

    page.get_by_role("button", name="Login").click()

    expect(page).to_have_url(
    "http://127.0.0.1:8000/accounts/login/"
)

# --- CP-029 - Usuario inexistente
def test_login_usuario_inexistente(page: Page):

    page.goto("http://127.0.0.1:8000/accounts/login/")

    page.get_by_label("Username").fill("noexiste")
    page.get_by_label("Password").fill("cualquiera123")

    page.get_by_role("button", name="Login").click()

    expect(page).to_have_url(
    "http://127.0.0.1:8000/accounts/login/"
)


#--- CP-030 - Contraseña incorrecta
def test_login_contrasena_incorrecta(page: Page):

    page.goto("http://127.0.0.1:8000/accounts/login/")

    page.get_by_label("Username").fill("hp")
    page.get_by_label("Password").fill("incorrecto")

    page.get_by_role("button", name="Login").click()

    expect(page).to_have_url(
    "http://127.0.0.1:8000/accounts/login/"
)
