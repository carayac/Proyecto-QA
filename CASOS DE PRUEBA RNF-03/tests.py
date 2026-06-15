"""
Pruebas automatizadas - RNF-03: Usabilidad sobre la emision de productos
Atributo de calidad: Usabilidad

Aplicacion bajo prueba: Stock Management System (Django)
Vista bajo prueba: stock.views.issue_item  ->  URL name 'issue_item'

Estas son las pruebas automatizadas del requerimiento NO FUNCIONAL RNF-03
(usabilidad). Verifican aspectos comprobables por codigo: el idioma del mensaje
de confirmacion y la claridad de la accion en la pantalla de emision. Se
complementan con la auditoria de accesibilidad de Google Lighthouse (WCAG 2.1)
y con la evaluacion heuristica de Nielsen, que son herramienta/manual y no
requieren codigo propio. Los casos CP-RNF03-03 (pluralizacion del mensaje) y
CP-RNF03-04 (recuperacion ante errores) se evaluaron de forma manual/heuristica.

Las pruebas FUNCIONALES de RF-03 estan en "CASOS DE PRUEBA RF-03\tests.py".

Como ejecutar (desde la raiz del proyecto, con el entorno virtual activo):

    # 1) copiar este archivo dentro de la app 'stock'
    Copy-Item "CASOS DE PRUEBA RNF-03\tests.py" "stock\tests_rnf03_usab.py" -Force
    # 2) correr solo esta suite
    python manage.py test stock.tests_rnf03_usab -v 2
    # 3) (opcional) borrar la copia
    Remove-Item "stock\tests_rnf03_usab.py"

Cada metodo corresponde a un caso documentado (CP-RNF03-xx). Los metodos que
FALLAN documentan defectos reales de usabilidad registrados en la matriz de
defectos (la falla ES la evidencia del defecto).
"""
from django.contrib.auth.models import User as AuthUser
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from stock.models import Category, Stock


class UsabilidadEmisionTests(TestCase):
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

    def test_cp_rnf03_01_mensaje_confirmacion_en_espanol(self):
        """CP-RNF03-01 -> DEF-06: el mensaje de confirmacion deberia estar en espanol."""
        self.client.force_login(self.user)
        resp = self.client.post(self.url, {"issue_quantity": 1, "issued_to": "Cliente Ana"})
        mensajes = " ".join(self._mensajes(resp)).lower()
        self.assertTrue(
            any(p in mensajes for p in ("emitido", "correctamente", "exito", "unidades")),
            "DEF-06: la interfaz/mensajes de emision estan solo en ingles",
        )

    def test_cp_rnf03_02_pantalla_emision_tiene_accion_clara(self):
        """CP-RNF03-02 -> DEF-05: la pantalla de emision debe etiquetar la accion como 'Emitir'."""
        self.client.force_login(self.user)
        resp = self.client.get(self.url)
        contenido = resp.content.decode().lower()
        self.assertIn(
            "emitir", contenido,
            "DEF-05: la pantalla reusa el formulario 'Add Stock' sin una accion clara de emision",
        )
