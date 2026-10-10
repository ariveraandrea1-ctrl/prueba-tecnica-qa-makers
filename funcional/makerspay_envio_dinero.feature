# language: es
# Especificación de comportamiento (BDD). Este archivo no tiene un runner: MakersPay es un
# producto ficticio, así que los escenarios documentan el comportamiento esperado y quedan
# listos para automatizarse con una herramienta como behave o pytest-bdd cuando exista la app.
@makerspay @envio_dinero
Característica: Envío de dinero entre usuarios de MakersPay
  Como usuario autenticado de MakersPay
  Quiero enviar dinero a otro usuario registrado usando su número de celular
  Para transferir fondos de forma rápida y segura

  Antecedentes:
    Dado que existe la usuaria "Ana" con celular "3001112233" y saldo de $100.000 COP
    Y existe el usuario "Carlos" con celular "3104445566" y saldo de $50.000 COP
    Y "Ana" ha iniciado sesión en MakersPay

  @smoke @positivo
  Escenario: Envío exitoso a un usuario registrado
    Cuando "Ana" envía $20.000 COP al celular "3104445566"
    Entonces se muestra el mensaje de envío exitoso
    Y el saldo de "Ana" es $80.000 COP
    Y el saldo de "Carlos" es $70.000 COP
    Y el movimiento aparece en el historial de "Ana" y de "Carlos"

  @limites
  Esquema del escenario: Validación de los montos mínimo y máximo por transacción
    Dado que el saldo de "Ana" es $3.000.000 COP
    Cuando "Ana" envía <monto> COP al celular "3104445566"
    Entonces el resultado de la transacción es "<resultado>"

    Ejemplos:
      | monto      | resultado                              |
      | $4.999     | Rechazada: monto menor al mínimo       |
      | $5.000     | Exitosa                                |
      | $5.001     | Exitosa                                |
      | $1.999.999 | Exitosa                                |
      | $2.000.000 | Exitosa                                |
      | $2.000.001 | Rechazada: monto mayor al máximo       |

  @negativo
  Escenario: Envío rechazado por saldo insuficiente
    Cuando "Ana" intenta enviar $100.001 COP al celular "3104445566"
    Entonces se muestra el mensaje de saldo insuficiente
    Y el saldo de "Ana" sigue siendo $100.000 COP
    Y el saldo de "Carlos" sigue siendo $50.000 COP
    Y no se registra ningún movimiento en los historiales

  @negativo
  Escenario: Envío rechazado al propio número de celular
    Cuando "Ana" intenta enviar $20.000 COP al celular "3001112233"
    Entonces se muestra el mensaje "No puedes enviarte dinero a ti mismo"
    Y el saldo de "Ana" sigue siendo $100.000 COP

  @negativo
  Escenario: Envío rechazado a un número no registrado
    Cuando "Ana" intenta enviar $20.000 COP al celular "3209998877"
    Entonces se muestra el mensaje de número no registrado en MakersPay
    Y el saldo de "Ana" sigue siendo $100.000 COP

  @seguridad
  Escenario: Intento de envío sin sesión iniciada
    Dado que "Ana" cerró sesión
    Cuando intenta acceder a la opción "Enviar dinero"
    Entonces la app solicita iniciar sesión
    Y no se procesa ninguna transacción

  @concurrencia
  Escenario: Doble toque en el botón "Confirmar" no duplica el envío
    Cuando "Ana" ingresa $20.000 COP para el celular "3104445566"
    Y toca "Confirmar" dos veces seguidas
    Entonces se procesa una sola transacción
    Y el saldo de "Ana" es $80.000 COP
    Y aparece un solo movimiento en su historial