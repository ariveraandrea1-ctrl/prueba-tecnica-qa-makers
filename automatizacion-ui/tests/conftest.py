import os
from pathlib import Path

import pytest
from selenium import webdriver

# Carpeta donde se guardan las capturas de cada prueba
SCREENSHOTS_DIR = Path(__file__).resolve().parents[2] / "evidencias" / "capturas" / "ui"


@pytest.fixture
def driver(request):
    """Abre Chrome antes de cada prueba y lo cierra al terminar, guardando una captura."""
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1366,768")

    # Desactiva las ventanas del gestor de contraseñas de Chrome,
    # que pueden tapar la página e interrumpir la prueba
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    })
    options.add_argument("--disable-features=PasswordLeakDetection")

    # Ejecutar sin abrir ventana: HEADLESS=true pytest
    if os.getenv("HEADLESS", "false").lower() == "true":
        options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)
    yield driver

    # Al terminar cada prueba: guardar captura como evidencia
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    driver.save_screenshot(str(SCREENSHOTS_DIR / f"{request.node.name}.png"))
    driver.quit()