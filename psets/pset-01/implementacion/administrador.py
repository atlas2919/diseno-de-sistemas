# Actor Administrador. Responsable de RN-07 y RN-08.


class Administrador:
    def __init__(self, identificador, nombre):
        self._id = identificador
        self._nombre = nombre

    @property
    def id(self):
        return self._id

    @property
    def nombre(self):
        return self._nombre

    def agregar_cancha(self, complejo, cancha):
        # CU-03 · Registrar cancha (RF-14).
        return complejo.agregar_cancha(cancha)

    def deshabilitar_cancha(self, cancha):
        # CU-04 · Deshabilitar cancha (RF-15).
        return cancha.deshabilitar()

    def consultar_conflictos(self, complejo):
        # CU-08 · Consultar conflictos pendientes (RF-16).
        return complejo.conflictos_pendientes()

    def resolver_conflicto(self, conflicto, decision, momento_actual):
        # CU-05 · Resolver conflicto (RF-17).
        return conflicto.resolver(self, decision, momento_actual)