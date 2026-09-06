# Entidad Conflicto. Da contenido a RN-08.


class Conflicto:
    def __init__(self, identificador, reserva_desplazada, reserva_ganadora,
                 momento):
        self._id = identificador
        self._reserva_desplazada = reserva_desplazada
        self._reserva_ganadora = reserva_ganadora
        self._momento = momento
        self._resuelto = False
        self._resolucion = None
        self._resuelto_por = None
        self._momento_resolucion = None

    @property
    def id(self):
        return self._id

    @property
    def reserva_desplazada(self):
        return self._reserva_desplazada

    @property
    def reserva_ganadora(self):
        return self._reserva_ganadora

    @property
    def momento(self):
        return self._momento

    @property
    def resolucion(self):
        return self._resolucion

    def esta_pendiente(self):
        return not self._resuelto

    def resolver(self, administrador, decision, momento_actual):
        if self._resuelto:
            return False
        self._resuelto = True
        self._resolucion = decision
        self._resuelto_por = administrador.nombre
        self._momento_resolucion = momento_actual
        return True