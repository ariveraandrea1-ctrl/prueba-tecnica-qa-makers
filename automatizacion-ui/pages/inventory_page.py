from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class InventoryPage:
    """Page Object de la página de productos (después del login)."""

    TITLE = (By.CSS_SELECTOR, "[data-test='title']")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def get_title(self):
        """Devuelve el título de la página (debería ser 'Products')."""
        return self.wait.until(EC.visibility_of_element_located(self.TITLE)).text

    def is_loaded(self):
        """Confirma que la URL corresponde a la página de inventario."""
        return "inventory.html" in self.driver.current_url