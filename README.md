# Prueba técnica QA Full Stack – Makers Solutions

Andrea Rivera Amador · [LinkedIn](https://linkedin.com/in/andrea-rivera-qa) · Octubre 2026

Este repositorio contiene mi solución a la prueba técnica para el cargo de QA Full Stack. La prueba tenía tres partes y las organicé en carpetas separadas:

- `automatizacion-ui/`: smoke test del login de SauceDemo con Selenium y Python.
- `api/`: pruebas del API de reqres.in, primero en Postman y luego automatizadas con pytest.
- `funcional/`: diseño de pruebas para MakersPay, la billetera ficticia del enunciado.

Las evidencias, los reportes y la matriz de ejecución están en `evidencias/`.

---

## Plan de pruebas

**Objetivo.** Verificar el inicio de sesión de SauceDemo, el flujo de creación y consulta de usuarios del API de reqres.in, y dejar diseñadas las pruebas del envío de dinero en MakersPay.

**Alcance**

| Módulo | Qué probé | Qué quedó por fuera |
|---|---|---|
| UI (SauceDemo) | Login exitoso, contraseña incorrecta, campos obligatorios, usuario bloqueado y usuario inexistente | Carrito, checkout y el resto de la tienda |
| API (reqres.in) | `POST /users`, `GET /users/{id}`, casos negativos y autenticación | Otros endpoints y pruebas de carga |
| Funcional (MakersPay) | Análisis del requerimiento y diseño de escenarios, casos, bugs y Gherkin | La ejecución, porque la aplicación no existe |

**Enfoque y herramientas**

- UI: pruebas automatizadas con Selenium WebDriver, pytest y Page Object Model.
- API: pruebas manuales en Postman y luego automatizadas con pytest y requests.
- Funcional: partición de equivalencia, valores límite, tabla de decisión, transición de estados y adivinación de errores. Los escenarios principales están escritos en Gherkin.

**Ambiente.** macOS, Python 3.14 y Google Chrome. SauceDemo en https://www.saucedemo.com y reqres.in en https://reqres.in/api, que ahora pide una clave gratuita en el header `x-api-key`.

**Criterios de entrada.** Los sitios de SauceDemo y reqres.in disponibles, la clave del API configurada en `.env` y las dependencias instaladas.

**Criterios de salida.** Todos los casos de UI y API ejecutados, y cada falla documentada con su evidencia y registrada como Issue.

**Casos de prueba y ejecución.** Los documenté en [`MATRIZ_EJECUCION_PRUEBAS.xlsx`](evidencias/MATRIZ_EJECUCION_PRUEBAS.xlsx), con una hoja por módulo: datos de la prueba, pasos, resultado esperado, resultado obtenido, estatus y enlace al defecto. La misma información está en [CSV](evidencias/MATRIZ_EJECUCION_PRUEBAS.csv) para verla directamente en GitHub.

**Riesgos**

- reqres.in es un API de demostración y no guarda lo que se crea (ver H-01).
- Los servicios externos pueden cambiar sin aviso; durante la prueba reqres.in empezó a exigir `x-api-key`.
- Los casos de MakersPay quedan diseñados, pero no se pueden ejecutar.

---

## Resultados

| Módulo | Resultado |
|---|---|
| UI (SauceDemo) | 7 de 7 pruebas pasan |
| API (reqres.in) | De 6 pruebas, 4 pasan y 2 fallan por hallazgos que documenté (en pytest están como `xfail`) |
| Funcional (MakersPay) | 20 escenarios, 22 casos de prueba, 2 bugs ficticios y escenarios en Gherkin |

- Casos de prueba y ejecución: [Excel](evidencias/MATRIZ_EJECUCION_PRUEBAS.xlsx) y [CSV](evidencias/MATRIZ_EJECUCION_PRUEBAS.csv)
- Reporte de pytest: [`reporte_completo.html`](evidencias/reporte_completo.html) (hay que descargarlo y abrirlo en el navegador)
- Bugs y hallazgos: [Issues del repositorio](https://github.com/ariveraandrea1-ctrl/prueba-tecnica-qa-makers/issues), organizados en este [tablero de GitHub Projects](https://github.com/users/ariveraandrea1-ctrl/projects/1)

---

## Cómo ejecutar las pruebas

Necesitas Python 3.10 o superior (lo probé con Python 3.14) y Google Chrome. Selenium descarga el driver automáticamente.

```bash
git clone https://github.com/ariveraandrea1-ctrl/prueba-tecnica-qa-makers.git
cd prueba-tecnica-qa-makers
python3 -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

En `requirements.txt` solo están las dependencias directas del proyecto; pip instala el resto automáticamente.

Las pruebas de API necesitan una clave gratuita de reqres.in, que se crea en [app.reqres.in](https://app.reqres.in/api-keys). Copia la plantilla y pon tu clave:

```bash
cp .env.example .env
```

```
REQRES_API_KEY=tu_clave_de_reqres
```

El archivo `.env` está en el `.gitignore`, así que la clave no se sube al repositorio.

Para correr las pruebas:

```bash
# Todo (API + UI) con reporte HTML
python -m pytest -v --html=evidencias/reporte_completo.html --self-contained-html

# Solo API
python -m pytest api/tests -v

# Solo el smoke test de UI
python -m pytest -m smoke -v

# UI sin abrir el navegador
HEADLESS=true python -m pytest automatizacion-ui/tests -v
```

---

## 1. Automatización UI (SauceDemo)

Automaticé el smoke test del login con Selenium y pytest. Además de los tres casos que pedía el enunciado, agregué el usuario bloqueado y un usuario que no existe.

| ID | Caso | Resultado |
|---|---|---|
| CP-UI-01 | Login exitoso | Pasó |
| CP-UI-02 | Contraseña incorrecta | Pasó |
| CP-UI-03 | Campos obligatorios (ambos vacíos, usuario vacío, contraseña vacía) | Pasó (3 de 3) |
| CP-UI-04 | Usuario bloqueado | Pasó |
| CP-UI-05 | Usuario inexistente | Pasó |

Algunas decisiones que tomé:

- Usé Page Object Model para que los localizadores estén en `pages/` y no repartidos por las pruebas.
- Las esperas son explícitas (`WebDriverWait`), sin `sleep`.
- Los localizadores usan `id` y `data-test`, que son los más estables en SauceDemo.
- Cada prueba abre un navegador nuevo y guarda una captura al terminar en `evidencias/capturas/ui/`.
- Los casos de campos obligatorios usan `parametrize` para no repetir código.

---

## 2. API (reqres.in)

El enunciado pedía crear un usuario con `POST /users`, tomar el `id` y consultarlo con `GET /users/{id}`. Primero lo probé en Postman y luego lo automaticé con pytest.

| ID | Caso | Esperado | Obtenido |
|---|---|---|---|
| CP-API-01 | Crear usuario | 201 | 201 |
| CP-API-02 | Consultar el usuario creado | 200 | 404 |
| CP-API-03 | Consultar un usuario existente | 200 | 200 |
| CP-API-04 | Consultar usuarios inexistentes (23 y 999) | 404 | 404 |
| CP-API-05 | Crear usuario sin `x-api-key` | 401 o 403 | 201 |

En el camino encontré cuatro cosas:

- **H-01 (media):** el usuario creado con `POST` no se puede consultar con `GET` porque reqres.in no guarda los datos. Es una limitación del entorno, pero impide validar el flujo completo.
- **H-02 (alta):** el `POST` acepta solicitudes sin `x-api-key`, aunque la documentación dice que es obligatoria.
- **H-03 (baja):** el `id` llega como texto en el `POST` y como número en el `GET`.
- **H-04 (baja):** el `404` llega con el body vacío, sin mensaje de error.

Las pruebas de CP-API-02 y CP-API-05 están marcadas como `xfail` con la referencia al hallazgo. Usé `strict=True` para que pytest avise si el comportamiento del API cambia y la prueba empieza a pasar.

Las capturas de Postman y el detalle de cada caso están en [`EVIDENCIAS_API.md`](evidencias/EVIDENCIAS_API.md) (también en PDF). La colección de Postman está en [`api/postman/reqres_collection.json`](api/postman/reqres_collection.json); para usarla hay que crear un Environment con la variable `api_key`.

---

## 3. Pruebas funcionales (MakersPay)

MakersPay es una billetera ficticia, así que en este módulo no hay ejecución: el trabajo está en el diseño. En [`PRUEBAS_FUNCIONALES_MAKERSPAY.md`](funcional/PRUEBAS_FUNCIONALES_MAKERSPAY.md) (también en PDF) están:

- Las 8 reglas de negocio que saqué del requerimiento y 12 preguntas que le haría al equipo, con los supuestos que tomé mientras tanto.
- Las técnicas que usé y los tipos de prueba que aplicarían.
- 20 escenarios y 22 casos de prueba con datos concretos.
- 2 bugs ficticios: un envío que descuenta el saldo pero no le llega al destinatario, y el botón "Confirmar" que no se habilita en Android.

Los escenarios principales también están en Gherkin, en [`makerspay_envio_dinero.feature`](funcional/makerspay_envio_dinero.feature). Ese archivo es una especificación en formato BDD: no tiene un runner porque la aplicación no existe, pero los escenarios quedan listos para automatizarse con behave o pytest-bdd.

---

## Estructura

```
prueba-tecnica-qa-makers/
├── automatizacion-ui/
│   ├── pages/            # Page Objects (login e inventario)
│   └── tests/            # Pruebas de login
├── api/
│   ├── tests/            # Pruebas con pytest + requests
│   └── postman/          # Colección de Postman
├── funcional/            # Documento de MakersPay (md y pdf) y archivo .feature
├── evidencias/           # Evidencias de API, capturas, matriz de ejecución y reporte HTML
├── .env.example
├── pytest.ini
└── requirements.txt
```
