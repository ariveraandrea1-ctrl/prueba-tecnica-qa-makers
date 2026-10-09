import os

import pytest
from dotenv import load_dotenv

# Carga las variables del archivo .env (ahí está la clave de reqres)
load_dotenv()

BASE_URL = "https://reqres.in/api"


@pytest.fixture(scope="session")
def base_url():
    """URL base de la API, compartida por todas las pruebas."""
    return BASE_URL


@pytest.fixture(scope="session")
def api_key():
    """Lee la clave desde la variable de entorno REQRES_API_KEY."""
    key = os.getenv("REQRES_API_KEY")
    if not key:
        pytest.skip("Falta REQRES_API_KEY en el archivo .env (ver .env.example)")
    return key


@pytest.fixture(scope="session")
def headers(api_key):
    """Headers estándar para las solicitudes autenticadas."""
    return {
        "x-api-key": api_key,
        "Content-Type": "application/json",
    }