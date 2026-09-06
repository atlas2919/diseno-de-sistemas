# Agregado que custodia el catalogo de canchas y el registro de conflictos.


class ComplejoDeportivo:
    def __init__(self, nombre):
        self._nombre = nombre
        self._canchas = []
        self._conflictos = []

    @property
    def nombre(self):
        return self._nombre

    @property
    def total_conflictos(self):
        return len(self._conflictos)

    def agregar_cancha(self, cancha):
        if self.cancha_por_id(cancha.id) is not None:
            return False
        self._canchas.append(cancha)
        cancha.registrar_en(self)
        return True

    def cancha_por_id(self, identificador):
        for cancha in self._canchas:
            if cancha.id == identificador:
                return cancha
        return None

    def canchas_habilitadas(self):
        return [c for c in self._canchas if c.esta_habilitada]

    def registrar_conflicto(self, conflicto):
        self._conflictos.append(conflicto)

    def conflictos_pendientes(self):
        # CU-08 · Consultar conflictos pendientes (RF-16).
        return [c for c in self._conflictos if c.esta_pendiente()]