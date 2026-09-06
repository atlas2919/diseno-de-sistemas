"""Simulacion de ReservaU.

Recorre todos los flujos documentados en el entregable de casos de uso. El orden
de los print() corresponde paso a paso al flujo principal y a los flujos alternos
de cada caso de uso.

El dominio no imprime nada: devuelve objetos resultado y este script los narra.
Esa separacion es lo que cumple RNF-05.

Ningun metodo del dominio consulta el reloj del sistema. El momento actual se
inyecta como parametro, por lo que la salida es identica en cada ejecucion
(RNF-04).
"""

from datetime import datetime

from administrador import Administrador
from cancha import Cancha
from complejo_deportivo import ComplejoDeportivo
from franja_horaria import FranjaHoraria
from solicitante import CapitanEquipo, Estudiante

# ----------------------------------------------------------------------------
# Momento actual fijo. Toda la simulacion ocurre "ahora" = lunes 11/05 08:00.
# ----------------------------------------------------------------------------
AHORA = datetime(2026, 5, 11, 8, 0)

FRANJA_PROXIMA = FranjaHoraria(datetime(2026, 5, 11, 9, 30),
                               datetime(2026, 5, 11, 11, 0))
FRANJA_TARDE = FranjaHoraria(datetime(2026, 5, 11, 14, 0),
                             datetime(2026, 5, 11, 16, 0))
FRANJA_NOCHE = FranjaHoraria(datetime(2026, 5, 11, 19, 0),
                             datetime(2026, 5, 11, 21, 0))

ANCHO = 74


def escenario(titulo):
    print()
    print("=" * ANCHO)
    print(f" {titulo}")
    print("=" * ANCHO)


def paso(numero, texto):
    print(f"  {numero:>5}. {texto}")


def nota(texto):
    print(f"         -> {texto}")


def main():
    print("=" * ANCHO)
    print(" SIMULACION ReservaU")
    print(f" Momento actual de la simulacion: {AHORA.strftime('%d/%m/%Y %H:%M')}")
    print("=" * ANCHO)

    # ------------------------------------------------------------------------
    # Instancias
    # ------------------------------------------------------------------------
    complejo = ComplejoDeportivo("Complejo Deportivo Universitario")

    diego = Administrador("AD-01", "Diego")
    ana = Estudiante("ES-01", "Ana")
    bruno = Estudiante("ES-02", "Bruno")
    carla = CapitanEquipo("CP-01", "Carla", "Seleccion de futbol")

    cancha_futbol = Cancha("CA-01", "Cancha de futbol")
    cancha_basquet = Cancha("CA-02", "Cancha de basquet")
    cancha_tenis = Cancha("CA-03", "Cancha de tenis")

    print()
    print(" Actores y su politica de prioridad:")
    for actor in (ana, bruno, carla):
        print(f"   - {actor.nombre:<8} ({type(actor).__name__:<13}) "
              f"-> {actor.politica()}")
    print(f"   - {diego.nombre:<8} (Administrador)")

    # ========================================================================
    escenario("ESCENARIO 1 - CU-03 Registrar cancha - flujo principal")
    # ========================================================================
    for cancha in (cancha_futbol, cancha_basquet, cancha_tenis):
        paso("1", f"{diego.nombre} solicita incorporar '{cancha.nombre}' "
                  f"al catalogo.")
        paso("2", "El sistema verifica que no exista otra cancha con el mismo "
                  "identificador.")
        aceptada = diego.agregar_cancha(complejo, cancha)
        paso("3", "El sistema incorpora la cancha al catalogo en estado "
                  "habilitada.")
        paso("4", f"El sistema informa: cancha {cancha.id} registrada "
                  f"({'aceptada' if aceptada else 'rechazada'}).")
        print()

    # ========================================================================
    escenario("ESCENARIO 2 - CU-03 alterno 2a - identificador duplicado")
    # ========================================================================
    duplicada = Cancha("CA-01", "Cancha de futbol (copia)")
    paso("1", f"{diego.nombre} solicita incorporar '{duplicada.nombre}' "
              f"al catalogo.")
    paso("2", "El sistema verifica que no exista otra cancha con el mismo "
              "identificador.")
    aceptada = diego.agregar_cancha(complejo, duplicada)
    paso("2a.1", "El sistema rechaza la operacion e informa la duplicidad.")
    nota(f"resultado: {'aceptada' if aceptada else 'rechazada'} - "
         f"CA-01 ya existe en el catalogo")
    paso("2a.2", "El caso de uso termina.")

    # ========================================================================
    escenario("ESCENARIO 3 - CU-01 Reservar cancha - flujo principal")
    # ========================================================================
    paso("1", f"{ana.nombre} solicita reservar '{cancha_futbol.nombre}' "
              f"para {FRANJA_TARDE.texto()}.")
    paso("2", "El sistema verifica que la cancha este habilitada.")
    nota(f"habilitada = {cancha_futbol.esta_habilitada}")
    paso("3", "El sistema verifica que la franja horaria no este ocupada.")
    nota(f"reserva vigente en la franja = "
         f"{cancha_futbol.reserva_vigente_en(FRANJA_TARDE)}")
    resultado = ana.reservar(cancha_futbol, FRANJA_TARDE, AHORA)
    reserva_ana = resultado.reserva
    paso("4", f"El sistema registra la reserva {reserva_ana.id} en estado "
              f"{reserva_ana.estado.value}.")
    paso("5", "El sistema informa al solicitante que la reserva quedo "
              "confirmada.")

    # ========================================================================
    escenario("ESCENARIO 4 - CU-01 alterno 3b - franja ocupada, sin prioridad")
    # ========================================================================
    paso("1", f"{bruno.nombre} solicita reservar '{cancha_futbol.nombre}' "
              f"para {FRANJA_TARDE.texto()}.")
    paso("2", "El sistema verifica que la cancha este habilitada.")
    paso("3", "El sistema verifica que la franja horaria no este ocupada.")
    nota(f"ocupada por {reserva_ana.id}")
    nota(f"{bruno.nombre} tiene prioridad para esa franja = "
         f"{bruno.tiene_prioridad_para(FRANJA_TARDE)}")
    resultado = bruno.reservar(cancha_futbol, FRANJA_TARDE, AHORA)
    paso("3b.1", "El sistema rechaza la solicitud sin alterar la reserva "
                 "existente.")
    nota(f"motivo: {resultado.motivo_rechazo}")
    nota(f"{reserva_ana.id} sigue en estado {reserva_ana.estado.value}")
    paso("3b.2", "El sistema informa que la franja no esta disponible.")
    paso("3b.3", "El caso de uso termina.")

    # ========================================================================
    escenario("ESCENARIO 5 - CU-01 alterno 3a + CU-06 - desplazamiento por "
              "prioridad")
    # ========================================================================
    paso("1", f"{carla.nombre} solicita reservar '{cancha_futbol.nombre}' "
              f"para {FRANJA_TARDE.texto()}.")
    paso("2", "El sistema verifica que la cancha este habilitada.")
    paso("3", "El sistema verifica que la franja horaria no este ocupada.")
    nota(f"ocupada por {reserva_ana.id}")
    nota(f"{carla.nombre} tiene prioridad para esa franja = "
         f"{carla.tiene_prioridad_para(FRANJA_TARDE)} "
         f"(inicia 14:00, antes de las 18:00)")
    paso("3a.1", "El sistema ejecuta CU-06 - Desplazar reserva por prioridad.")
    resultado = carla.reservar(cancha_futbol, FRANJA_TARDE, AHORA)
    reserva_carla = resultado.reserva
    print()
    print("       CU-06 - Desplazar reserva por prioridad")
    paso("1", f"El sistema cambia el estado de {resultado.reserva_desplazada.id} "
              f"a {resultado.reserva_desplazada.estado.value}.")
    paso("2", "El sistema libera la franja horaria que ocupaba esa reserva.")
    nota(f"{resultado.reserva_desplazada.id} vigente = "
         f"{resultado.reserva_desplazada.esta_vigente()}")
    paso("3", f"El sistema registra el conflicto {resultado.conflicto.id}.")
    paso("4", "El sistema devuelve el control a CU-01, paso 4.")
    print()
    paso("4", f"El sistema registra la reserva {reserva_carla.id} en estado "
              f"{reserva_carla.estado.value}.")
    paso("5", "El sistema informa al solicitante que la reserva quedo "
              "confirmada.")

    # ========================================================================
    escenario("ESCENARIO 6 - CU-01 alterno 3b - prioridad que NO aplica "
              "despues de las 18:00")
    # ========================================================================
    resultado = bruno.reservar(cancha_basquet, FRANJA_NOCHE, AHORA)
    reserva_bruno = resultado.reserva
    print(f"  (previo) {bruno.nombre} reserva '{cancha_basquet.nombre}' "
          f"{FRANJA_NOCHE.texto()} -> {reserva_bruno.id}")
    print()
    paso("1", f"{carla.nombre} solicita reservar '{cancha_basquet.nombre}' "
              f"para {FRANJA_NOCHE.texto()}.")
    paso("2", "El sistema verifica que la cancha este habilitada.")
    paso("3", "El sistema verifica que la franja horaria no este ocupada.")
    nota(f"ocupada por {reserva_bruno.id}")
    nota(f"{carla.nombre} tiene prioridad para esa franja = "
         f"{carla.tiene_prioridad_para(FRANJA_NOCHE)} "
         f"(inicia 19:00, despues de las 18:00)")
    resultado = carla.reservar(cancha_basquet, FRANJA_NOCHE, AHORA)
    paso("3b.1", "El sistema rechaza la solicitud sin alterar la reserva "
                 "existente.")
    nota(f"motivo: {resultado.motivo_rechazo}")
    paso("3b.2", "El sistema informa que la franja no esta disponible.")
    paso("3b.3", "El caso de uso termina.")

    # ========================================================================
    escenario("ESCENARIO 7 - CU-02 Cancelar reserva - flujo principal "
              "(anticipacion >= 2 h)")
    # ========================================================================
    paso("1", f"{bruno.nombre} solicita cancelar {reserva_bruno.id}.")
    paso("2", "El sistema verifica que el solicitante sea el titular.")
    nota(f"es titular = {reserva_bruno.es_titular(bruno)}")
    paso("3", "El sistema calcula la anticipacion respecto al inicio "
              "de la franja.")
    nota(f"anticipacion = {reserva_bruno.horas_hasta_inicio(AHORA):.2f} h")
    resultado = bruno.cancelar(reserva_bruno, AHORA)
    paso("4", f"El sistema determina que la anticipacion es de 2 h o mas y "
              f"registra la accion como {resultado.estado_resultante.value}.")
    paso("5", "El sistema libera la franja horaria.")
    nota(f"{reserva_bruno.id} vigente = {reserva_bruno.esta_vigente()}")
    paso("6", f"El sistema informa la clasificacion registrada: "
              f"{resultado.estado_resultante.value}.")

    # ========================================================================
    escenario("ESCENARIO 8 - CU-02 alterno 4a + CU-07 - no-show "
              "(anticipacion < 2 h)")
    # ========================================================================
    resultado = ana.reservar(cancha_tenis, FRANJA_PROXIMA, AHORA)
    reserva_proxima = resultado.reserva
    print(f"  (previo) {ana.nombre} reserva '{cancha_tenis.nombre}' "
          f"{FRANJA_PROXIMA.texto()} -> {reserva_proxima.id}")
    print()
    paso("1", f"{ana.nombre} solicita cancelar {reserva_proxima.id}.")
    paso("2", "El sistema verifica que el solicitante sea el titular.")
    nota(f"es titular = {reserva_proxima.es_titular(ana)}")
    paso("3", "El sistema calcula la anticipacion respecto al inicio "
              "de la franja.")
    nota(f"anticipacion = {reserva_proxima.horas_hasta_inicio(AHORA):.2f} h, "
         f"menor al minimo de 2 h")
    paso("4a.1", "El sistema ejecuta CU-07 - Registrar no-show.")
    resultado = ana.cancelar(reserva_proxima, AHORA)
    print()
    print("       CU-07 - Registrar no-show")
    paso("1", f"El sistema registra la accion como "
              f"{resultado.estado_resultante.value} en lugar de cancelacion regular.")
    paso("2", "El sistema deja constancia del cambio de estado con su momento "
              "y su motivo.")
    nota(f"{reserva_proxima.historial[-1].motivo}")
    paso("3", "El sistema devuelve el control a CU-02, paso 5.")
    print()
    paso("5", "El sistema libera la franja horaria.")
    paso("6", f"El sistema informa la clasificacion registrada: "
              f"{resultado.estado_resultante.value}.")
    nota("el solicitante nunca eligio esta clasificacion: la determino el "
         "sistema")

    # ========================================================================
    escenario("ESCENARIO 9 - CU-02 alterno 2a - cancelacion por quien no es "
              "titular")
    # ========================================================================
    paso("1", f"{bruno.nombre} solicita cancelar {reserva_carla.id}, "
              f"cuyo titular es {reserva_carla.titular.nombre}.")
    paso("2", "El sistema verifica que el solicitante sea el titular.")
    nota(f"es titular = {reserva_carla.es_titular(bruno)}")
    resultado = bruno.cancelar(reserva_carla, AHORA)
    paso("2a.1", "El sistema rechaza la cancelacion sin alterar la reserva.")
    nota(f"motivo: {resultado.motivo_rechazo}")
    nota(f"{reserva_carla.id} sigue en estado {reserva_carla.estado.value}")
    paso("2a.2", "El caso de uso termina.")

    # ========================================================================
    escenario("ESCENARIO 10 - CU-04 Deshabilitar cancha - flujo principal")
    # ========================================================================
    paso("1", f"{diego.nombre} solicita deshabilitar "
              f"'{cancha_tenis.nombre}'.")
    paso("2", "El sistema verifica que la cancha este habilitada.")
    nota(f"habilitada = {cancha_tenis.esta_habilitada}")
    aplicada = diego.deshabilitar_cancha(cancha_tenis)
    paso("3", "El sistema cambia el estado de la cancha a deshabilitada.")
    paso("4", f"El sistema informa que la cancha quedo deshabilitada "
              f"({'cambio aplicado' if aplicada else 'sin cambios'}).")

    # ========================================================================
    escenario("ESCENARIO 11 - CU-04 alterno 2a - cancha ya deshabilitada")
    # ========================================================================
    paso("1", f"{diego.nombre} solicita deshabilitar "
              f"'{cancha_tenis.nombre}'.")
    paso("2", "El sistema verifica que la cancha este habilitada.")
    nota(f"habilitada = {cancha_tenis.esta_habilitada}")
    aplicada = diego.deshabilitar_cancha(cancha_tenis)
    paso("2a.1", f"El sistema informa que no hay cambios por aplicar "
                 f"({'cambio aplicado' if aplicada else 'sin cambios'}).")
    paso("2a.2", "El caso de uso termina.")

    # ========================================================================
    escenario("ESCENARIO 12 - CU-01 alterno 2a - reserva sobre cancha "
              "deshabilitada")
    # ========================================================================
    paso("1", f"{bruno.nombre} solicita reservar '{cancha_tenis.nombre}' "
              f"para {FRANJA_TARDE.texto()}.")
    paso("2", "El sistema verifica que la cancha este habilitada.")
    nota(f"habilitada = {cancha_tenis.esta_habilitada}")
    resultado = bruno.reservar(cancha_tenis, FRANJA_TARDE, AHORA)
    paso("2a.1", "El sistema rechaza la solicitud e informa que la cancha no "
                 "esta disponible.")
    nota(f"motivo: {resultado.motivo_rechazo}")
    paso("2a.2", "El caso de uso termina.")

    # ========================================================================
    escenario("ESCENARIO 13 - CU-05 + CU-08 - resolver conflicto")
    # ========================================================================
    paso("1", f"{diego.nombre} solicita los conflictos pendientes de "
              f"resolucion.")
    paso("2", "El sistema ejecuta CU-08 - Consultar conflictos pendientes.")
    print()
    print("       CU-08 - Consultar conflictos pendientes")
    pendientes = diego.consultar_conflictos(complejo)
    paso("1", "El sistema recupera los conflictos aun no resueltos.")
    paso("2", "El sistema entrega cada conflicto con su reserva desplazada, "
              "su reserva ganadora y el momento.")
    for conflicto in pendientes:
        nota(f"{conflicto.id}: desplazada {conflicto.reserva_desplazada.id} "
             f"({conflicto.reserva_desplazada.titular.nombre}) - ganadora "
             f"{conflicto.reserva_ganadora.id} "
             f"({conflicto.reserva_ganadora.titular.nombre})")
    print()
    conflicto = pendientes[0]
    decision = ("Se reubica a Ana en la Cancha de basquet en la misma franja; "
                "se confirma la prioridad del equipo oficial.")
    paso("3", f"{diego.nombre} selecciona {conflicto.id} y registra su "
              f"decision.")
    nota(f"decision: {decision}")
    resuelto = diego.resolver_conflicto(conflicto, decision, AHORA)
    paso("4", "El sistema marca el conflicto como resuelto y almacena la "
              "decision.")
    nota(f"pendiente = {conflicto.esta_pendiente()}")
    paso("5", f"El sistema informa que el conflicto quedo resuelto "
              f"({'aplicado' if resuelto else 'sin cambios'}).")

    # ========================================================================
    escenario("ESCENARIO 14 - CU-05 alterno 3a - conflicto ya resuelto")
    # ========================================================================
    paso("3", f"{diego.nombre} selecciona {conflicto.id} y registra una "
              f"segunda decision.")
    resuelto = diego.resolver_conflicto(conflicto, "Otra decision", AHORA)
    paso("3a.1", f"El sistema rechaza la operacion e informa que el conflicto "
                 f"no esta pendiente ({'aplicado' if resuelto else 'rechazado'}).")
    paso("3a.2", "El caso de uso termina.")

    # ========================================================================
    escenario("ESTADO FINAL")
    # ========================================================================
    print(f"  {complejo.nombre}: "
          f"{len(complejo.canchas_habilitadas())} canchas habilitadas, "
          f"{complejo.total_conflictos} conflictos registrados")
    print()
    print("  Reservas por cancha:")
    for cancha in (cancha_futbol, cancha_basquet, cancha_tenis):
        estado_cancha = "habilitada" if cancha.esta_habilitada else "deshabilitada"
        print(f"    {cancha.nombre} ({estado_cancha})")
        for reserva in cancha.reservas:
            print(f"      - {reserva.id} [{reserva.franja.texto()}] "
                  f"titular {reserva.titular.nombre} - {reserva.estado.value}")
    print()
    print("  Historial de la reserva desplazada "
          f"({conflicto.reserva_desplazada.id}):")
    for registro in conflicto.reserva_desplazada.historial:
        anterior = registro.estado_anterior.value if registro.estado_anterior else "-"
        print(f"    {registro.momento.strftime('%d/%m %H:%M')}  "
              f"{anterior} -> {registro.estado_nuevo.value}: {registro.motivo}")
    print()
    print(f"  Conflictos pendientes: "
          f"{len(complejo.conflictos_pendientes())}")
    print()
    print("=" * ANCHO)
    print(" FIN DE LA SIMULACION")
    print("=" * ANCHO)


if __name__ == "__main__":
    main()