from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class LoginPage:
    """Page Object de la pantalla de inicio de sesión de SauceDemo."""

    URL = "https://www.saucedemo.com/"

    # Localizadores
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self):
        """Abre la página de login y espera a que cargue el formulario."""
        self.driver.get(self.URL)
        self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT))
        return self

    def login(self, username, password):
        """Escribe usuario y contraseña y hace clic en Login."""
        self._type(self.USERNAME_INPUT, username)
        self._type(self.PASSWORD_INPUT, password)
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    def get_error_message(self):
        """Devuelve el texto del mensaje de error."""
        return self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE)).text

    def _type(self, locator, text):
        """Limpia el campo y escribe el texto (si se envía vacío, lo deja vacío)."""
        field = self.wait.until(EC.visibility_of_element_located(locator))
        field.clear()
        if text:
            field.send_keys(text)