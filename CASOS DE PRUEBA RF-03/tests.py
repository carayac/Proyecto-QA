"""
Pruebas automatizadas - RF-03: Emitir productos a clientes (issue_item)
Atributo de calidad: Adecuacion funcional (RF-03)

Aplicacion bajo prueba: Stock Management System (Django)
Vista bajo prueba: stock.views.issue_item  ->  URL name 'issue_item'

Estas son las pruebas FUNCIONALES del requerimiento RF-03. Las pruebas de
usabilidad (RNF-03) estan en "CASOS DE PRUEBA RNF-03\tests.py".

Como ejecutar (desde la raiz del proyecto, con el entorno virtual activo):

    # 1) copiar este archivo dentro de la app 'stock'
    Copy-Item "CASOS DE PRUEBA RF-03\tests.py" "stock\tests_rf03_func.py" -Force
    # 2) correr solo esta suite
    python manage.py test stock.tests_rf03_func -v 2
    # 3) (opcional) borrar la copia
    Remove-Item "stock\tests_rf03_func.py"

Cada metodo corresponde a un caso documentado (CP-RF03-xx) en 01_casos-de-prueba.md.
Los metodos que FALLAN documentan defectos reales registrados en
03_matriz-de-defectos.md (la falla ES la evidencia del defecto).
"""
from django.contrib.auth.models import User as AuthUser
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from stock.models import Category, Stock, StockHistory


class EmitirProductosTests(TestCase):
    def setUp(self):
        self.user = AuthUser.objects.create_user(username="tester", password="tester-pass")
        self.category = Category.objects.create(group="Bebidas")
        self.item = Stock.objects.create(
            category=self.category,
            item_name="Jugo de Naranja",
            quantity=10,
            date=timezone.now(),
        )
        self.url = reverse("issue_item", args=[self.item.id])

    def _mensajes(self, response):
        return [str(m) for m in get_messages(response.wsgi_request)]

    # ------------------ Casos que deben PASAR (comportamiento correcto) ------------------

    def test_cp_rf03_01_emitir_cantidad_valida_reduce_stock(self):
        """CP-RF03-01: emitir 4 de 10 deja 6 unidades y registra cliente y responsable."""
        self.client.force_login(self.user)
        resp = self.client.post(self.url, {"issue_quantity": 4, "issued_to": "Cliente Ana"})
        self.item.refresh_from_db()
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(self.item.quantity, 6)
        self.assertEqual(self.item.issued_to, "Cliente Ana")
        self.assertEqual(self.item.issued_by, "tester")

    def test_cp_rf03_02_emitir_requiere_autenticacion(self):
        """CP-RF03-02: un usuario no autenticado es redirigido al login (control de acceso)."""
        resp = self.client.post(self.url, {"issue_quantity": 1, "issued_to": "X"})
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/accounts/login", resp.url)

    def test_cp_rf03_03_emitir_mas_que_existencias_se_rechaza(self):
        """CP-RF03-03: emitir 50 de 10 no modifica el stock y avisa 'Insufficient Stock'."""
        self.client.force_login(self.user)
        resp = self.client.post(self.url, {"issue_quantity": 50, "issued_to": "Cliente Ana"})
        self.item.refresh_from_db()
        self.assertEqual(self.item.quantity, 10)
        self.assertTrue(
            any("insufficient" in m.lower() or "insuficiente" in m.lower() for m in self._mensajes(resp)),
            "Se esperaba un aviso de stock insuficiente",
        )

    # ------------- Casos que FALLAN a proposito: documentan defectos reales -------------

    def test_cp_rf03_04_emitir_cantidad_negativa_debe_rechazarse(self):
        """CP-RF03-04 -> DEF-01: emitir cantidad negativa NO debe aumentar el inventario."""
        self.client.force_login(self.user)
        self.client.post(self.url, {"issue_quantity": -3, "issued_to": "Cliente Ana"})
        self.item.refresh_from_db()
        self.assertEqual(
            self.item.quantity, 10,
            "DEF-01: emitir una cantidad negativa AUMENTO el inventario (10 -> %s)" % self.item.quantity,
        )

    def test_cp_rf03_05_emitir_sin_cliente_debe_rechazarse(self):
        """CP-RF03-05 -> DEF-02: no se debe poder emitir sin indicar el cliente (issued_to)."""
        self.client.force_login(self.user)
        self.client.post(self.url, {"issue_quantity": 2, "issued_to": ""})
        self.item.refresh_from_db()
        self.assertEqual(
            self.item.quantity, 10,
            "DEF-02: se emitio producto sin registrar al cliente (issued_to vacio)",
        )

    def test_cp_rf03_06_emision_debe_registrar_historial(self):
        """CP-RF03-06 -> DEF-03: cada emision deberia generar un registro en StockHistory."""
        self.client.force_login(self.user)
        self.client.post(self.url, {"issue_quantity": 4, "issued_to": "Cliente Ana"})
        self.assertGreaterEqual(
            StockHistory.objects.count(), 1,
            "DEF-03: la emision no genera historial; no hay trazabilidad de movimientos",
        )

    def test_cp_rf03_07_emitir_cero_no_debe_reportar_exito(self):
        """CP-RF03-07 -> DEF-04: emitir 0 unidades no deberia reportarse como exito."""
        self.client.force_login(self.user)
        resp = self.client.post(self.url, {"issue_quantity": 0, "issued_to": "Cliente Ana"})
        exito = any("successfully" in m.lower() or "correctamente" in m.lower() for m in self._mensajes(resp))
        self.assertFalse(
            exito,
            "DEF-04: emitir 0 unidades se reporta como emision exitosa",
        )

    def test_cp_rf03_08_emitir_sin_cantidad_no_debe_romper(self):
        """CP-RF03-08 -> DEF-07: emitir con la cantidad vacia no debe provocar un error 500."""
        self.client.force_login(self.user)
        try:
            self.client.post(self.url, {"issue_quantity": "", "issued_to": "Cliente Ana"})
        except Exception as exc:
            self.fail("DEF-07: emitir sin cantidad provoco una excepcion no controlada: %r" % exc)
        self.item.refresh_from_db()
        self.assertEqual(self.item.quantity, 10)
