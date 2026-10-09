# Prueba técnica QA Full Stack – Makers Solutions

Solución de la prueba técnica para el rol de **QA Full Stack**, organizada en tres módulos: automatización de UI, pruebas de API y diseño de pruebas funcionales.

**Autora:** Andrea Rivera Amador · [LinkedIn](https://linkedin.com/in/andrea-rivera-qa) · Octubre 2026

---

## 📊 Resumen de resultados

| Módulo | Sobre qué | Resultado |
|---|---|---|
| **Automatización UI** | Smoke test de login en [SauceDemo](https://www.saucedemo.com/) | ✅ 7 de 7 pruebas pasan |
| **API** | Usuarios en [reqres.in](https://reqres.in/) | ✅ 4 pasan · ⚠️ 2 fallas esperadas y documentadas (`xfail`) |
| **Funcional** | Billetera ficticia **MakersPay** | 📝 20 escenarios · 22 casos de prueba · 2 bugs · Gherkin |

📄 Reporte HTML completo de la ejecución: [`evidencias/reporte_completo.html`](evidencias/reporte_completo.html) *(descárgalo y ábrelo en el navegador)*

---

## 🗂️ Estructura del proyecto

```
prueba-tecnica-qa-makers/
├── automatizacion-ui/          # Módulo de automatización (Selenium + POM)
│   ├── pages/                  # Page Objects: login e inventario
│   └── tests/                  # Pruebas de login (smoke test)
├── api/                        # Módulo de API
│   ├── tests/                  # Pruebas automatizadas con pytest + requests
│   └── postman/                # Colección de Postman exportada
├── funcional/                  # Módulo funcional (MakersPay)
│   ├── PRUEBAS_FUNCIONALES_MAKERSPAY.md
│   └── makerspay_envio_dinero.feature
├── evidencias/                 # Evidencias y reportes
│   ├── EVIDENCIAS_API.md       # Evidencias de las pruebas de API en Postman
│   ├── capturas/               # Capturas de Postman y de las pruebas de UI
│   └── reporte_completo.html   # Reporte de pytest
├── .env.example                # Plantilla de variables de entorno
├── pytest.ini                  # Configuración de pytest
└── requirements.txt            # Dependencias de Python
```

---

## 🛠️ Tecnologías

- **Python 3** · **pytest** · **pytest-html**
- **Selenium WebDriver** con el patrón **Page Object Model**
- **requests** para las pruebas de API
- **Postman** para las pruebas manuales de API
- **Gherkin** para la especificación BDD
- **python-dotenv** para el manejo seguro de credenciales

---

## ▶️ Cómo ejecutar las pruebas

### 1. Clonar el repositorio

```bash
git clone https://github.com/ariveraandrea1-ctrl/prueba-tecnica-qa-makers.git
cd prueba-tecnica-qa-makers
```

### 2. Crear el entorno virtual e instalar dependencias

```bash
python3 -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configurar la clave de la API

La API de reqres.in requiere una clave gratuita, que se obtiene en [app.reqres.in](https://app.reqres.in/api-keys).

```bash
cp .env.example .env
```

Luego abre `.env` y reemplaza el valor por tu clave:

```
REQRES_API_KEY=tu_clave_de_reqres
```

> El archivo `.env` está excluido del repositorio para no exponer credenciales.

### 4. Ejecutar

```bash
# Todas las pruebas (API + UI) con reporte HTML
python -m pytest -v --html=evidencias/reporte_completo.html --self-contained-html

# Solo las pruebas de API
python -m pytest api/tests -v

# Solo el smoke test de UI
python -m pytest -m smoke -v

# UI sin abrir el navegador (modo headless)
HEADLESS=true python -m pytest automatizacion-ui/tests -v
```

> Requiere Google Chrome instalado. Selenium Manager descarga automáticamente el driver.

---

## 🤖 Módulo 1: Automatización UI (SauceDemo)

Smoke test del inicio de sesión con **Selenium + pytest**, aplicando el patrón **Page Object Model**.

| ID | Caso | Resultado |
|---|---|---|
| CP-UI-01 | Login exitoso con credenciales válidas | ✅ |
| CP-UI-02 | Login fallido con contraseña incorrecta | ✅ |
| CP-UI-03 | Campos obligatorios: ambos vacíos, usuario vacío, contraseña vacía | ✅ ✅ ✅ |
| CP-UI-04 | Usuario bloqueado *(caso adicional)* | ✅ |
| CP-UI-05 | Usuario inexistente *(caso adicional)* | ✅ |

**Buenas prácticas aplicadas:**

- **Page Object Model:** los localizadores están separados de las pruebas.
- **Esperas explícitas** (`WebDriverWait`) en lugar de pausas fijas.
- **Localizadores estables** (`id` y `data-test`).
- **Fixtures de pytest:** un navegador nuevo por prueba, con cierre garantizado.
- **Captura automática** de pantalla al final de cada prueba (`evidencias/capturas/ui/`).
- **`parametrize`** para cubrir varias combinaciones sin repetir código.

---

## 🔌 Módulo 2: API (reqres.in)

Flujo solicitado: `POST /users` → extraer el `id` → `GET /users/{id}` → validar `name` y `job`.

| ID | Caso | Esperado | Obtenido | Estado |
|---|---|---|---|---|
| CP-API-01 | Crear usuario | 201 | 201 | ✅ |
| CP-API-02 | Consultar usuario creado | 200 | 404 | ⚠️ `xfail` (H-01) |
| CP-API-03 | Consultar usuario existente | 200 | 200 | ✅ |
| CP-API-04 | Consultar usuarios inexistentes (23 y 999) | 404 | 404 | ✅ |
| CP-API-05 | Crear usuario sin API key | 401 / 403 | 201 | ⚠️ `xfail` (H-02) |

### Hallazgos

| ID | Hallazgo | Severidad |
|---|---|---|
| **H-01** | El usuario creado con `POST` no se puede consultar con `GET`: la API es de demostración y no guarda los datos | Media |
| **H-02** | El endpoint permite crear usuarios **sin** `x-api-key`, aunque la documentación indica que es obligatoria | Alta |
| **H-03** | El `id` se devuelve como texto en `POST` y como número en `GET` | Baja |
| **H-04** | La respuesta `404` llega sin mensaje de error | Baja |

> Las pruebas CP-API-02 y CP-API-05 están marcadas como `xfail` (falla esperada) con la referencia a su hallazgo. Usan `strict=True`, así que si el comportamiento de la API cambia, pytest lo notifica.

📄 Evidencias detalladas con capturas: [`evidencias/EVIDENCIAS_API.md`](evidencias/EVIDENCIAS_API.md)

### Colección de Postman

Importa [`api/postman/reqres_collection.json`](api/postman/reqres_collection.json) en Postman y crea un **Environment** con la variable `api_key` y tu clave de reqres.in.

---

## 📝 Módulo 3: Pruebas funcionales (MakersPay)

**MakersPay** es una billetera digital ficticia definida en el enunciado. Este módulo presenta el **diseño** de las pruebas:

- **Análisis del requerimiento:** 8 reglas de negocio y 12 preguntas o ambigüedades, con los supuestos asumidos.
- **Técnicas:** partición de equivalencia, valores límite, tabla de decisión, transición de estados y adivinación de errores.
- **Tipos de prueba:** funcional, negativa, integración, seguridad, usabilidad, compatibilidad, concurrencia, regresión y API.
- **20 escenarios y 22 casos de prueba** con datos concretos y trazabilidad a las reglas.
- **2 bugs ficticios críticos:** saldo descontado sin acreditar al destinatario, y botón "Confirmar" deshabilitado en Android.
- **Escenarios en Gherkin** (BDD), incluido un esquema con tabla de ejemplos para los valores límite.

📄 [`funcional/PRUEBAS_FUNCIONALES_MAKERSPAY.md`](funcional/PRUEBAS_FUNCIONALES_MAKERSPAY.md)
🥒 [`funcional/makerspay_envio_dinero.feature`](funcional/makerspay_envio_dinero.feature)