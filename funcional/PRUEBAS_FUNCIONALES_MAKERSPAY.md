# Pruebas funcionales – MakersPay

**Prueba técnica QA Full Stack – Makers Solutions**
Andrea Rivera Amador · Octubre 2026

> **Nota:** MakersPay es un producto ficticio definido en el enunciado de la prueba. Este documento presenta el **diseño** de las pruebas (análisis, técnicas, escenarios y casos), que estarían listas para ejecutarse cuando la aplicación esté disponible. Los bugs del apartado 5 son **ficticios** y representan hallazgos realistas que podrían detectarse al ejecutar estos casos.

---

## 1. Análisis del requerimiento

**Requerimiento:** un usuario autenticado puede enviar dinero a otro usuario registrado usando su número de celular.

### 1.1 Reglas de negocio identificadas

| ID | Regla |
|---|---|
| RN-01 | Solo un usuario autenticado puede enviar dinero |
| RN-02 | El destinatario debe ser un usuario registrado, identificado por su número de celular |
| RN-03 | Monto mínimo por transacción: $5.000 COP |
| RN-04 | Monto máximo por transacción: $2.000.000 COP |
| RN-05 | No se puede enviar más dinero que el saldo disponible |
| RN-06 | No se permiten envíos al propio número de celular |
| RN-07 | Si la transacción es exitosa: se descuenta el saldo del remitente, se incrementa el del destinatario y se registra el movimiento en el historial de ambos |
| RN-08 | Si la transacción falla: se muestra un mensaje de error claro y no se afecta ningún saldo |

### 1.2 Preguntas y ambigüedades para aclarar con el equipo

| # | Pregunta | Por qué importa |
|---|---|---|
| P-01 | ¿Los montos de $5.000 y $2.000.000 están **incluidos** en el rango permitido? | Define los valores límite exactos que se deben probar (4.999 / 5.000 y 2.000.000 / 2.000.001). |
| P-02 | ¿Se permiten montos con decimales o centavos? Si no, ¿cómo se maneja una entrada como $5.000,50? | Afecta la validación del campo de monto y el cálculo de los saldos. |
| P-03 | ¿Existe un límite de transacciones o de monto acumulado por día? ¿Y hacia un mismo número? | Son reglas comunes en billeteras (prevención de fraude y normativa) que no están especificadas. |
| P-04 | ¿Se puede iniciar una transacción sin conexión a internet? | Define el comportamiento esperado de la app sin red. |
| P-05 | Si la conexión se pierde durante la transacción, ¿qué pasa cuando se recupera? ¿Se reintenta, se cancela o queda pendiente? | Riesgo de envíos duplicados, de dinero descontado sin llegar al destinatario o de saldos inconsistentes. |
| P-06 | ¿Qué pasa si el número de destino no está registrado en MakersPay? ¿Se muestra un error o se invita al destinatario a registrarse? | El requerimiento solo cubre usuarios registrados. |
| P-07 | ¿Qué pasa si la cuenta del destinatario está bloqueada o inactiva? | Debe definirse si se rechaza el envío y qué mensaje ve el remitente. |
| P-08 | ¿Qué formato de celular es válido? ¿Solo números colombianos de 10 dígitos que empiezan por 3? ¿Se aceptan números extranjeros o con indicativo (+57)? | Define las clases válidas e inválidas del campo de celular. |
| P-09 | ¿Cuál es el texto exacto de cada mensaje de error (saldo insuficiente, monto fuera de rango, envío a sí mismo, número no registrado)? ¿Se valida antes o después de confirmar? | RN-08 exige mensajes claros, pero no los define. Sin textos, no se puede validar el resultado esperado con precisión. |
| P-10 | ¿Hay comisión por envío? Si la hay, ¿se descuenta del monto o del saldo? | Cambia el cálculo del saldo final y la validación de RN-05 y RN-07. |
| P-11 | ¿Qué pasa si el usuario toca "Enviar" dos veces seguidas o hace dos envíos simultáneos? | Riesgo de transacciones duplicadas o de enviar más del saldo disponible. |
| P-12 | ¿En qué plataformas está disponible MakersPay (Android, iOS, web)? ¿Qué versiones mínimas y navegadores se soportan? | Define la matriz de compatibilidad: en qué dispositivos y navegadores se deben ejecutar las pruebas. |

> **Supuestos para esta prueba:** mientras no haya respuesta, se asume que los límites son **inclusivos** (5.000 y 2.000.000 son válidos), que **no se aceptan decimales**, que **no hay comisión** y que el celular válido es **colombiano de 10 dígitos que empieza por 3**.

---

## 2. Técnicas y tipos de prueba

### 2.1 Técnicas de diseño de pruebas

#### a) Partición de equivalencia
Se dividen los datos de entrada en grupos que el sistema debería tratar igual, y se prueba un valor representativo de cada grupo.

**Campo monto:**

| Clase | Rango / ejemplo | Tipo |
|---|---|---|
| CE-M1 | Menor a $5.000 (ej. $3.000) | Inválida |
| CE-M2 | Entre $5.000 y $2.000.000 (ej. $50.000) | Válida |
| CE-M3 | Mayor a $2.000.000 (ej. $3.000.000) | Inválida |
| CE-M4 | Mayor al saldo disponible | Inválida |
| CE-M5 | Cero, negativo, decimales o texto (ej. $0, -$10.000, $5.000,50, "abc") | Inválida |

**Campo celular del destinatario:**

| Clase | Ejemplo | Tipo |
|---|---|---|
| CE-C1 | Celular registrado de otro usuario | Válida |
| CE-C2 | Celular con formato válido pero no registrado | Inválida |
| CE-C3 | Celular propio del remitente | Inválida |
| CE-C4 | Formato inválido (9 dígitos, letras, no empieza por 3) | Inválida |
| CE-C5 | Campo vacío | Inválida |

#### b) Análisis de valores límite
Los errores suelen aparecer justo en los bordes de un rango, así que se prueba el límite, el valor anterior y el siguiente.

| Límite | Valor | Resultado esperado |
|---|---|---|
| Mínimo | $4.999 | Rechazado |
| Mínimo | $5.000 | Permitido |
| Mínimo | $5.001 | Permitido |
| Máximo | $1.999.999 | Permitido |
| Máximo | $2.000.000 | Permitido |
| Máximo | $2.000.001 | Rechazado |
| Saldo (ej. $100.000) | $99.999 | Permitido |
| Saldo (ej. $100.000) | $100.000 (todo el saldo) | Permitido |
| Saldo (ej. $100.000) | $100.001 | Rechazado |

#### c) Tabla de decisión
Combina las condiciones de negocio para ver el resultado de cada combinación. **Se lee por columnas:** cada columna (R1 a R6) es una situación distinta.

| Condición | R1 | R2 | R3 | R4 | R5 | R6 |
|---|---|---|---|---|---|---|
| Usuario autenticado | Sí | No | Sí | Sí | Sí | Sí |
| Destinatario registrado | Sí | – | No | Sí | Sí | Sí |
| Destinatario ≠ remitente | Sí | – | – | No | Sí | Sí |
| Monto entre $5.000 y $2.000.000 | Sí | – | – | – | No | Sí |
| Monto ≤ saldo disponible | Sí | – | – | – | – | No |
| **Resultado** | Envío exitoso | Pide iniciar sesión | Destinatario no registrado | Envío a sí mismo | Monto fuera de rango | Saldo insuficiente |

*(–) = no se evalúa, porque una condición anterior ya rechazó la transacción.*

#### d) Transición de estados
Una transacción pasa por varios estados, y se verifica que cada cambio sea correcto.

`Iniciada` → `Validada` → `Confirmada por el usuario` → `Exitosa` o `Fallida`

- De **Validada** solo se avanza si se cumplen todas las reglas.
- Si queda **Fallida**, ningún saldo cambia (RN-08).
- Una transacción **Exitosa** no puede volver a procesarse (evita duplicados).

#### e) Adivinación de errores (error guessing)
Casos basados en la experiencia, donde suelen aparecer fallas:
- Tocar "Enviar" dos veces seguidas.
- Perder la conexión justo al confirmar.
- Celular con espacios, guiones o indicativo (+57 300 123 4567).
- Sesión expirada en medio del envío.
- Dos envíos simultáneos desde dos dispositivos que juntos superan el saldo.

### 2.2 Tipos de prueba

| Tipo | Qué se valida en MakersPay |
|---|---|
| **Funcional** | Que el envío cumpla todas las reglas de negocio (RN-01 a RN-08). |
| **Negativa** | Que el sistema rechace correctamente los datos y situaciones inválidas. |
| **De integración** | Que el descuento al remitente, el abono al destinatario y el registro en ambos historiales ocurran juntos y de forma consistente. |
| **De seguridad** | Que no se pueda enviar sin autenticación, con la sesión expirada o manipulando la solicitud (por ejemplo, alterando el monto en la API). |
| **De usabilidad** | Que los mensajes de error sean claros y comprensibles para el usuario. |
| **De compatibilidad** | Que el envío de dinero funcione igual en Android, iOS y los navegadores soportados (Chrome, Safari, Firefox, Edge). |
| **De concurrencia / rendimiento** | Que no se dupliquen transacciones con doble clic o envíos simultáneos, y que el tiempo de respuesta sea aceptable. |
| **De regresión** | Que, después de cada cambio en la app, el envío de dinero siga funcionando como antes. |
| **De API** | Validar las reglas directamente en el servicio, sin pasar por la interfaz. |

---

## 3. Escenarios de prueba

| ID | Escenario | Regla | Técnica | Prioridad |
|---|---|---|---|---|
| ESC-01 | Enviar dinero exitosamente a otro usuario registrado | RN-02, RN-07 | Tabla de decisión (R1) | Alta |
| ESC-02 | Intentar enviar dinero sin haber iniciado sesión | RN-01 | Tabla de decisión (R2) | Alta |
| ESC-03 | Enviar el monto mínimo permitido | RN-03 | Valores límite | Alta |
| ESC-04 | Enviar el monto máximo permitido | RN-04 | Valores límite | Alta |
| ESC-05 | Intentar enviar menos del monto mínimo | RN-03 | Valores límite | Alta |
| ESC-06 | Intentar enviar más del monto máximo | RN-04 | Valores límite | Alta |
| ESC-07 | Enviar un monto igual al saldo disponible | RN-05 | Valores límite | Media |
| ESC-08 | Intentar enviar un monto mayor al saldo disponible | RN-05 | Tabla de decisión (R6) | Alta |
| ESC-09 | Verificar el descuento del saldo del remitente tras un envío exitoso | RN-07 | Partición de equivalencia | Alta |
| ESC-10 | Verificar el aumento del saldo del destinatario tras un envío exitoso | RN-07 | Partición de equivalencia | Alta |
| ESC-11 | Verificar que el movimiento aparezca en el historial de ambos usuarios | RN-07 | Partición de equivalencia | Media |
| ESC-12 | Verificar que una transacción fallida no afecte ningún saldo | RN-08 | Transición de estados | Alta |
| ESC-13 | Intentar enviar dinero al propio número de celular | RN-06 | Tabla de decisión (R4) | Alta |
| ESC-14 | Intentar enviar dinero a un número no registrado | RN-02 | Tabla de decisión (R3) | Alta |
| ESC-15 | Intentar enviar a un celular con formato inválido | RN-02 | Partición de equivalencia | Media |
| ESC-16 | Intentar enviar montos no válidos (cero, negativos, decimales o texto) | RN-03 | Partición de equivalencia | Media |
| ESC-17 | Tocar "Enviar" dos veces seguidas | RN-07 | Adivinación de errores | Alta |
| ESC-18 | Perder la conexión a internet al confirmar el envío | RN-08 | Adivinación de errores | Alta |
| ESC-19 | Intentar enviar con la sesión expirada | RN-01 | Adivinación de errores | Media |
| ESC-20 | Enviar dinero desde distintas plataformas y navegadores | RN-07 | Pruebas de compatibilidad | Alta |

---

## 4. Casos de prueba

### 4.1 Datos de prueba

| Usuario | Rol | Celular | Saldo inicial |
|---|---|---|---|
| Ana | Remitente | 3001112233 | $100.000 (o $3.000.000 cuando se indique) |
| Carlos | Destinatario registrado | 3104445566 | $50.000 |
| — | Número no registrado | 3209998877 | — |

> Salvo que se indique otra cosa, cada caso inicia con Ana autenticada y los saldos iniciales de la tabla.

### 4.2 Casos de prueba

| ID | Escenario | Precondiciones | Pasos | Datos | Resultado esperado | Prioridad |
|---|---|---|---|---|---|---|
| CP-F-01 | ESC-01 | Ana autenticada, saldo $100.000 | 1. Ir a "Enviar dinero"<br>2. Ingresar celular<br>3. Ingresar monto<br>4. Confirmar | 3104445566 · $20.000 | Mensaje de envío exitoso. La transacción queda en estado *Exitosa* | Alta |
| CP-F-02 | ESC-02 | Usuario sin sesión iniciada | 1. Abrir la app<br>2. Intentar entrar a "Enviar dinero" | — | La app pide iniciar sesión y no permite acceder al envío | Alta |
| CP-F-03 | ESC-03 | Ana autenticada, saldo $100.000 | Pasos 1 a 4 de CP-F-01 | 3104445566 · $5.000 | Envío exitoso. Saldo de Ana: $95.000 | Alta |
| CP-F-04 | ESC-03 | Ana autenticada, saldo $100.000 | Pasos 1 a 4 de CP-F-01 | 3104445566 · $5.001 | Envío exitoso. Saldo de Ana: $94.999 | Media |
| CP-F-05 | ESC-04 | Ana autenticada, saldo $3.000.000 | Pasos 1 a 4 de CP-F-01 | 3104445566 · $2.000.000 | Envío exitoso. Saldo de Ana: $1.000.000 | Alta |
| CP-F-06 | ESC-04 | Ana autenticada, saldo $3.000.000 | Pasos 1 a 4 de CP-F-01 | 3104445566 · $1.999.999 | Envío exitoso. Saldo de Ana: $1.000.001 | Media |
| CP-F-07 | ESC-05 | Ana autenticada, saldo $100.000 | Pasos 1 a 4 de CP-F-01 | 3104445566 · $4.999 | Mensaje: el monto mínimo es $5.000. Ningún saldo cambia | Alta |
| CP-F-08 | ESC-06 | Ana autenticada, saldo $3.000.000 | Pasos 1 a 4 de CP-F-01 | 3104445566 · $2.000.001 | Mensaje: el monto máximo es $2.000.000. Ningún saldo cambia | Alta |
| CP-F-09 | ESC-07 | Ana autenticada, saldo $100.000 | Pasos 1 a 4 de CP-F-01 | 3104445566 · $100.000 | Envío exitoso. Saldo de Ana: $0 | Media |
| CP-F-10 | ESC-08 | Ana autenticada, saldo $100.000 | Pasos 1 a 4 de CP-F-01 | 3104445566 · $100.001 | Mensaje de saldo insuficiente. Ningún saldo cambia | Alta |
| CP-F-11 | ESC-09 | CP-F-01 ejecutado con éxito | 1. Ir a la pantalla principal de Ana<br>2. Consultar el saldo | — | Saldo de Ana: $80.000 ($100.000 − $20.000) | Alta |
| CP-F-12 | ESC-10 | CP-F-01 ejecutado con éxito | 1. Iniciar sesión como Carlos<br>2. Consultar el saldo | — | Saldo de Carlos: $70.000 ($50.000 + $20.000) | Alta |
| CP-F-13 | ESC-11 | CP-F-01 ejecutado con éxito | 1. Revisar el historial de Ana<br>2. Revisar el historial de Carlos | — | Ana: movimiento de salida por $20.000 hacia 3104445566. Carlos: movimiento de entrada por $20.000 desde 3001112233. Ambos con fecha y hora | Media |
| CP-F-14 | ESC-12 | Ana autenticada, saldo $100.000 | 1. Ejecutar CP-F-10 (envío que falla)<br>2. Consultar el saldo y el historial de Ana y de Carlos | 3104445566 · $100.001 | Saldos sin cambios (Ana $100.000, Carlos $50.000). No aparece ningún movimiento nuevo en los historiales | Alta |
| CP-F-15 | ESC-13 | Ana autenticada, saldo $100.000 | Pasos 1 a 4 de CP-F-01 | 3001112233 (propio) · $20.000 | Mensaje: no puedes enviarte dinero a ti mismo. Ningún saldo cambia | Alta |
| CP-F-16 | ESC-14 | Ana autenticada, saldo $100.000 | Pasos 1 a 4 de CP-F-01 | 3209998877 · $20.000 | Mensaje: el número no está registrado en MakersPay. Ningún saldo cambia | Alta |
| CP-F-17 | ESC-15 | Ana autenticada | Pasos 1 y 2 de CP-F-01 con cada dato | 300123456 (9 dígitos) · 30011122ab · 2001112233 · campo vacío | Mensaje de formato de celular inválido en cada caso. No permite continuar | Media |
| CP-F-18 | ESC-16 | Ana autenticada | Pasos 1 a 3 de CP-F-01 con cada dato | $0 · −$10.000 · $5.000,50 · "abc" | El campo rechaza el valor o muestra mensaje de monto inválido. No permite continuar | Media |
| CP-F-19 | ESC-17 | Ana autenticada, saldo $100.000 | 1. Completar los pasos 1 a 3 de CP-F-01<br>2. Tocar "Confirmar" dos veces seguidas muy rápido | 3104445566 · $20.000 | Se procesa **una sola** transacción. Saldo de Ana: $80.000. Un solo movimiento en el historial | Alta |
| CP-F-20 | ESC-18 | Ana autenticada, saldo $100.000 | 1. Completar los pasos 1 a 3 de CP-F-01<br>2. Activar el modo avión<br>3. Tocar "Confirmar"<br>4. Desactivar el modo avión | 3104445566 · $20.000 | Mensaje claro de falta de conexión. Los saldos quedan consistentes: o la transacción se completa en ambos lados o no se realiza en ninguno (ver P-05) | Alta |
| CP-F-21 | ESC-19 | Ana autenticada y sesión expirada antes de confirmar | 1. Completar los pasos 1 a 3 de CP-F-01<br>2. Esperar a que expire la sesión<br>3. Tocar "Confirmar" | 3104445566 · $20.000 | La app pide iniciar sesión de nuevo y la transacción no se procesa | Media |
| CP-F-22 | ESC-20 | Ana autenticada, saldo $100.000, en cada plataforma | Pasos 1 a 4 de CP-F-01 en: Android, iOS, Chrome, Safari | 3104445566 · $20.000 | El envío es exitoso y se comporta igual en todas las plataformas. Saldo de Ana: $80.000 en cada ejecución (restaurando el saldo entre pruebas) | Alta |

**Cobertura:** los 22 casos cubren las 8 reglas de negocio (RN-01 a RN-08) y los 20 escenarios definidos.

---

## 5. Reporte de bugs (ficticios)

### BUG-01 – Se descuenta el saldo del remitente, pero no se acredita al destinatario

| Campo | Detalle |
|---|---|
| **Severidad** | Crítica |
| **Prioridad** | Alta |
| **Ambiente** | QA · App MakersPay v1.0 · iPhone 15 Pro · iOS 18 |
| **Casos relacionados** | CP-F-11, CP-F-12, CP-F-13 |
| **Regla incumplida** | RN-07 |
| **Precondiciones** | Ana autenticada, con saldo de $100.000. Carlos registrado (3104445566), con saldo de $50.000. |
| **Datos** | Celular 3104445566 · Monto $20.000 |
| **Pasos para reproducir** | 1. Ir a "Enviar dinero"<br>2. Ingresar el celular 3104445566<br>3. Ingresar el monto $20.000<br>4. Tocar "Confirmar"<br>5. Consultar el saldo y el historial de Ana<br>6. Iniciar sesión como Carlos y consultar su saldo y su historial |
| **Resultado esperado** | Saldo de Ana: $80.000, con el movimiento de salida en su historial. Saldo de Carlos: $70.000, con el movimiento de entrada en su historial. |
| **Resultado obtenido** | La app muestra "Envío exitoso". El saldo de Ana baja a $80.000 y el movimiento aparece en su historial, pero el saldo de Carlos sigue en $50.000 y no aparece ningún movimiento en su historial. |
| **Impacto** | El dinero se descuenta al remitente y no llega al destinatario: el usuario pierde su dinero. Afecta la confianza en la plataforma y puede generar reclamos y sanciones regulatorias. |
| **Frecuencia** | Siempre (100%) |
| **Evidencia** | Capturas del saldo y el historial de ambos usuarios, antes y después del envío |

### BUG-02 – El botón "Confirmar" no se habilita en Android al enviar dinero

| Campo | Detalle |
|---|---|
| **Severidad** | Crítica |
| **Prioridad** | Alta |
| **Ambiente donde falla** | QA · App MakersPay v1.0 · Samsung Galaxy S23 · Android 14 |
| **Ambiente donde funciona (control)** | QA · App MakersPay v1.0 · iPhone 15 Pro · iOS 18 |
| **Caso relacionado** | CP-F-22 |
| **Regla afectada** | RN-07 |
| **Precondiciones** | Ana autenticada en Android, con saldo de $100.000. Carlos registrado (3104445566). |
| **Datos** | Celular 3104445566 · Monto $20.000 |
| **Pasos para reproducir** | 1. Ir a "Enviar dinero"<br>2. Ingresar el celular 3104445566<br>3. Ingresar el monto $20.000<br>4. Observar el botón "Confirmar" |
| **Resultado esperado** | Con datos válidos, el botón "Confirmar" se habilita y permite completar el envío, igual que en iOS. |
| **Resultado obtenido** | En Android, el botón "Confirmar" permanece deshabilitado (en gris) aunque los datos son válidos. No es posible completar el envío. En iOS, con los mismos datos, el botón se habilita y el envío es exitoso. |
| **Impacto** | Ningún usuario de Android puede enviar dinero. |
| **Frecuencia** | Siempre (100%) |
| **Evidencia** | Video comparativo Android vs. iOS adjunto |

### Resumen de bugs

| ID | Título | Severidad | Prioridad | Estado |
|---|---|---|---|---|
| BUG-01 | Se descuenta el saldo del remitente, pero no se acredita al destinatario | Crítica | Alta | Abierto |
| BUG-02 | El botón "Confirmar" no se habilita en Android al enviar dinero | Crítica | Alta | Abierto |

---

## 6. Escenarios en Gherkin (BDD)

Los escenarios principales se especifican en lenguaje Gherkin en el archivo [`makerspay_envio_dinero.feature`](makerspay_envio_dinero.feature).