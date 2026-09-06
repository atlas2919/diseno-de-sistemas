# Entidad Reserva. Reglas RN-04, RN-05 y RN-06.

from estado_reserva import EstadoReserva

class RegistroEstado:
    def __init__(self, momento, estado_anterior, estado_nuevo, motivo):
        self.momento = momento
        self.estado_anterior = estado_anterior
        self.estado_nuevo = estado_nuevo
        self.motivo = motivo


class ResultadoCancelacion:
    def __init__(self, aceptada, estado_resultante=None,
                 horas_de_anticipacion=None, motivo_rechazo=None):
        self.aceptada = aceptada
        self.estado_resultante = estado_resultante
        self.horas_de_anticipacion = horas_de_anticipacion
        self.motivo_rechazo = motivo_rechazo


class Reserva:

    HORAS_MINIMAS_CANCELACION = 2

    def __init__(self, identificador, titular, cancha, franja,
                 momento_creacion):
        self._id = identificador
        self._titular = titular
        self._cancha = cancha
        self._franja = franja
        self._estado = EstadoReserva.CONFIRMADA
        self._historial = [
            RegistroEstado(
                momento_creacion, 
                None, 
                EstadoReserva.CONFIRMADA, 
                "creacion de la reserva"
                )
        ]

    @property
    def id(self):
        return self._id

    @property
    def titular(self):
        return self._titular

    @property
    def cancha(self):
        return self._cancha

    @property
    def franja(self):
        return self._franja

    @property
    def estado(self):
        return self._estado

    @property
    def historial(self):
        return list(self._historial)

    def es_titular(self, solicitante):
        return solicitante.id == self._titular.id

    def esta_vigente(self):
        return self._estado == EstadoReserva.CONFIRMADA

    def horas_hasta_inicio(self, momento_actual):
        return self._franja.horas_hasta(momento_actual)

    def cancelar(self, solicitante, momento_actual):
        if not self.esta_vigente():
            return ResultadoCancelacion(False, motivo_rechazo="la reserva ya esta en estado " + self._estado.value)

        if not self.es_titular(solicitante):
            return ResultadoCancelacion(False, motivo_rechazo="el solicitante no es el titular de la reserva")

        horas = self.horas_hasta_inicio(momento_actual)

        if horas < self.HORAS_MINIMAS_CANCELACION:
            nuevo = EstadoReserva.NO_SHOW
            comparacion = "menor"
        else:
            nuevo = EstadoReserva.CANCELADA
            comparacion = "igual o mayor"

        motivo = ("cancelacion con {:.2f} h de anticipacion, {} al minimo de {} h").format(horas, comparacion, self.HORAS_MINIMAS_CANCELACION)

        self._transicionar(nuevo, momento_actual, motivo)
        return ResultadoCancelacion(True, estado_resultante=nuevo, horas_de_anticipacion=horas)

    def desplazar(self, momento_actual, motivo):
        self._transicionar(EstadoReserva.DESPLAZADA, momento_actual, motivo)

    def _transicionar(self, nuevo, momento, motivo):
        self._historial.append(RegistroEstado(momento, self._estado, nuevo, motivo))
        self._estado = nuevo