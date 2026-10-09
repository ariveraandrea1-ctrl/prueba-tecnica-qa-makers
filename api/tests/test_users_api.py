import pytest
import requests

PAYLOAD = {"name": "Test User", "job": "Automation Engineer"}
TIMEOUT = 10  # segundos máximos de espera por respuesta


def crear_usuario(base_url, headers, payload=PAYLOAD):
    """Envía el POST para crear un usuario y devuelve la respuesta."""
    return requests.post(f"{base_url}/users", json=payload, headers=headers, timeout=TIMEOUT)


# ---------------------------------------------------------------------------
# CP-API-01: Crear usuario
# ---------------------------------------------------------------------------
def test_crear_usuario_retorna_201_con_datos_enviados(base_url, headers):
    response = crear_usuario(base_url, headers)

    assert response.status_code == 201, f"Se esperaba 201 y se obtuvo {response.status_code}"
    body = response.json()
    assert body["name"] == PAYLOAD["name"]
    assert body["job"] == PAYLOAD["job"]
    assert body.get("id"), "La respuesta no trae el id del usuario creado"
    assert "createdAt" in body


# ---------------------------------------------------------------------------
# CP-API-02: Flujo pedido en la prueba (POST -> extraer id -> GET)
# ---------------------------------------------------------------------------
@pytest.mark.xfail(
    reason="H-01: reqres.in es una API mock; el POST no guarda el usuario, por eso el GET devuelve 404",
    strict=True,
)
def test_flujo_crear_y_consultar_usuario_creado(base_url, headers):
    # 1. Crear el usuario
    post_response = crear_usuario(base_url, headers)
    assert post_response.status_code == 201

    # 2. Extraer el id del usuario recién creado
    user_id = post_response.json()["id"]

    # 3. Consultar el usuario con ese id
    get_response = requests.get(f"{base_url}/users/{user_id}", headers=headers, timeout=TIMEOUT)
    assert get_response.status_code == 200, f"Se esperaba 200 y se obtuvo {get_response.status_code}"

    # 4. Validar que los datos coincidan con los enviados
    data = get_response.json().get("data", get_response.json())
    assert data["name"] == PAYLOAD["name"]
    assert data["job"] == PAYLOAD["job"]


# ---------------------------------------------------------------------------
# CP-API-03: Consultar usuario existente
# ---------------------------------------------------------------------------
def test_consultar_usuario_existente_retorna_200(base_url, headers):
    response = requests.get(f"{base_url}/users/2", headers=headers, timeout=TIMEOUT)

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["id"] == 2
    for campo in ["email", "first_name", "last_name", "avatar"]:
        assert campo in data, f"Falta el campo '{campo}' en la respuesta"


# ---------------------------------------------------------------------------
# CP-API-04: Consultar usuarios inexistentes (caso negativo)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("user_id", [23, 999])
def test_consultar_usuario_inexistente_retorna_404(base_url, headers, user_id):
    response = requests.get(f"{base_url}/users/{user_id}", headers=headers, timeout=TIMEOUT)

    assert response.status_code == 404


# ---------------------------------------------------------------------------
# CP-API-05: Crear usuario sin API key (caso negativo de seguridad)
# ---------------------------------------------------------------------------
@pytest.mark.xfail(
    reason="H-02: el endpoint legacy acepta solicitudes sin x-api-key, contrario a la documentación",
    strict=True,
)
def test_crear_usuario_sin_api_key_es_rechazado(base_url):
    headers_sin_clave = {"Content-Type": "application/json"}
    response = crear_usuario(base_url, headers_sin_clave)

    assert response.status_code in (401, 403), f"Se esperaba 401/403 y se obtuvo {response.status_code}"