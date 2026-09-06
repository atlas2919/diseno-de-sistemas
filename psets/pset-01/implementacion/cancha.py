# Entidad Cancha. Dueña de RN-01 y de la aplicación mecánica de RN-03.

from conflicto import Conflicto
from reserva import Reserva

class ResultadoReserva:
    def __init__(self, aceptada, reserva=None, conflicto=None, reserva_desplazada=None, motivo_rechazo=None):
        self.aceptada = aceptada
        self.reserva = reserva
        self.conflicto = conflicto
        self.reserva_desplazada = reserva_desplazada
        self.motivo_rechazo = motivo_rechazo


class Cancha:
    def __init__(self, identificador, nombre):
        self._id = identificador
        self._nombre = nombre
        self._habilitada = True
        self._reservas = []
        self._complejo = None
        self._desplazamientos = 0

    @property
    def id(self):
        return self._id

    @property
    def nombre(self):
        return self._nombre

    @property
    def esta_habilitada(self):
        return self._habilitada

    @property
    def reservas(self):
        return list(self._reservas)

    def reserva_vigente_en(self, franja):
        for reserva in self._reservas:
            if reserva.esta_vigente() and reserva.franja.se_solapa_con(franja):
                return reserva
        return None

    def esta_disponible(self, franja):
        return self._habilitada and self.reserva_vigente_en(franja) is None

    def reservar_para(self, solicitante, franja, momento_actual):
        # CU-01 paso 2 y alterno 2a
        if not self._habilitada:
            return ResultadoReserva(
                False,
                motivo_rechazo="la cancha " + self._nombre + " esta deshabilitada")

        # CU-01 paso 3
        existente = self.reserva_vigente_en(franja)

        if existente is None:
            return ResultadoReserva(True, reserva=self._crear(solicitante, franja, momento_actual))

        # CU-01 alterno 3b: franja ocupada y sin prioridad
        if not solicitante.tiene_prioridad_para(franja):
            return ResultadoReserva(
                False,
                motivo_rechazo="la franja " + franja.texto() + " ya esta ocupada por " + existente.id)

        # CU-01 alterno 3a, que ejecuta CU-06
        return self._desplazar_por_prioridad(existente, solicitante, franja, momento_actual)

    def deshabilitar(self):
        if not self._habilitada:
            return False
        self._habilitada = False
        return True

    def habilitar(self):
        self._habilitada = True

    def registrar_en(self, complejo):
        self._complejo = complejo

    def _crear(self, solicitante, franja, momento_actual):
        identificador = "R-{}-{:02d}".format(self._id, len(self._reservas) + 1)
        reserva = Reserva(identificador, solicitante, self, franja, momento_actual)
        self._reservas.append(reserva)
        return reserva

    def _desplazar_por_prioridad(self, existente, solicitante, franja, momento_actual):
        # CU-06 · Desplazar reserva por prioridad.
        motivo = ("desplazada por prioridad de " + solicitante.nombre + " (" + solicitante.politica()+ ")")
        existente.desplazar(momento_actual, motivo)

        ganadora = self._crear(solicitante, franja, momento_actual)

        self._desplazamientos += 1
        conflicto = Conflicto(
            "CF-{}-{:02d}".format(self._id, self._desplazamientos),
            existente, ganadora, momento_actual)
        if self._complejo is not None:
            self._complejo.registrar_conflicto(conflicto)

        return ResultadoReserva(True, reserva=ganadora, conflicto=conflicto, reserva_desplazada=existente)