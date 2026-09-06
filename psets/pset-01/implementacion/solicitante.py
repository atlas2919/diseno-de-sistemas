# Actores capaces de reservar y cancelar.

from abc import ABC

from reglas_prioridad import PrioridadEquipoOficial, SinPrioridad


class Solicitante(ABC):
    # Esa ausencia es lo que evita el condicional dentro del metodo (RF-07).
    def __init__(self, identificador, nombre, regla_prioridad):
        self._id = identificador
        self._nombre = nombre
        self._regla_prioridad = regla_prioridad

    @property
    def id(self):
        return self._id

    @property
    def nombre(self):
        return self._nombre

    def politica(self):
        # Describe la politica de prioridad compuesta en este solicitante.
        return self._regla_prioridad.descripcion()

    def tiene_prioridad_para(self, franja):
        # Responde si posee prioridad sobre la franja, delegando en su regla.
        return self._regla_prioridad.aplica(franja)

    def reservar(self, cancha, franja, momento_actual):
        # Inicia una solicitud de reserva. La decision la toma la cancha.
        return cancha.reservar_para(self, franja, momento_actual)

    def cancelar(self, reserva, momento_actual):
        # Inicia la cancelacion. La clasificacion la determina la reserva.
        return reserva.cancelar(self, momento_actual)


class Estudiante(Solicitante):
    # Solicitante sin prioridad.

    def __init__(self, identificador, nombre):
        super().__init__(identificador, nombre, SinPrioridad())


class CapitanEquipo(Solicitante):
    # Solicitante que representa a un equipo oficial (RN-02).
    # Realiza exactamente las mismas acciones que un estudiante. La unica
    # diferencia es la politica de prioridad con que se construye.

    def __init__(self, identificador, nombre, equipo):
        super().__init__(identificador, nombre, PrioridadEquipoOficial())
        self._equipo = equipo

    @property
    def equipo(self):
        return self._equipo