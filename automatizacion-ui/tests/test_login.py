import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

# Todas las pruebas de este archivo forman parte del Smoke Test
pytestmark = pytest.mark.smoke

VALID_USER = "standard_user"
VALID_PASSWORD = "secret_sauce"

MSG_CREDENCIALES_INVALIDAS = "Epic sadface: Username and password do not match any user in this service"
MSG_USUARIO_REQUERIDO = "Epic sadface: Username is required"
MSG_CONTRASENA_REQUERIDA = "Epic sadface: Password is required"
MSG_USUARIO_BLOQUEADO = "Epic sadface: Sorry, this user has been locked out."


# ---------------------------------------------------------------------------
# CP-UI-01: Login exitoso con credenciales válidas
# ---------------------------------------------------------------------------
def test_login_exitoso_con_credenciales_validas(driver):
    LoginPage(driver).open().login(VALID_USER, VALID_PASSWORD)

    inventory = InventoryPage(driver)
    assert inventory.get_title() == "Products"
    assert inventory.is_loaded(), f"No se redirigió al inventario. URL actual: {driver.current_url}"


# ---------------------------------------------------------------------------
# CP-UI-02: Login fallido con contraseña incorrecta
# ---------------------------------------------------------------------------
def test_login_fallido_con_contrasena_incorrecta(driver):
    login = LoginPage(driver).open()
    login.login(VALID_USER, "clave_incorrecta")

    assert login.get_error_message() == MSG_CREDENCIALES_INVALIDAS
    assert "inventory.html" not in driver.current_url, "No debería permitir el acceso"


# ---------------------------------------------------------------------------
# CP-UI-03: Validación de campos obligatorios
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "usuario, contrasena, mensaje_esperado",
    [
        ("", "", MSG_USUARIO_REQUERIDO),
        ("", VALID_PASSWORD, MSG_USUARIO_REQUERIDO),
        (VALID_USER, "", MSG_CONTRASENA_REQUERIDA),
    ],
    ids=["ambos_vacios", "usuario_vacio", "contrasena_vacia"],
)
def test_validacion_campos_obligatorios(driver, usuario, contrasena, mensaje_esperado):
    login = LoginPage(driver).open()
    login.login(usuario, contrasena)

    assert login.get_error_message() == mensaje_esperado


# ---------------------------------------------------------------------------
# Casos adicionales
# ---------------------------------------------------------------------------
def test_login_usuario_bloqueado(driver):
    """CP-UI-04: un usuario bloqueado no puede ingresar."""
    login = LoginPage(driver).open()
    login.login("locked_out_user", VALID_PASSWORD)

    assert login.get_error_message() == MSG_USUARIO_BLOQUEADO


def test_login_usuario_inexistente(driver):
    """CP-UI-05: un usuario que no existe no puede ingresar."""
    login = LoginPage(driver).open()
    login.login("usuario_que_no_existe", VALID_PASSWORD)

    assert login.get_error_message() == MSG_CREDENCIALES_INVALIDAS