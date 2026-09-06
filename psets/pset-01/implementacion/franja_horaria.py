# Representa un intervalo de tiempo reservable.

class FranjaHoraria:
    def __init__(self, inicio, fin):
        if fin <= inicio:
            raise ValueError("La franja debe terminar despues de su inicio")
        self._inicio = inicio
        self._fin = fin

    @property
    def inicio(self):
        return self._inicio

    @property
    def fin(self):
        return self._fin

    def se_solapa_con(self, otra):
        # Indica si esta franja comparte algun instante con otra.
        return self._inicio < otra.fin and otra.inicio < self._fin

    def inicia_antes_de(self, hora):
        # Lo consulta PrioridadEquipoOficial para evaluar RN-03. El limite se
        # compara contra el inicio de la franja, segun el supuesto S-02.
        return self._inicio.time() < hora

    def horas_hasta(self, momento):
        # Horas que faltan hasta el inicio. Lo consulta Reserva para RN-05.
        return (self._inicio - momento).total_seconds() / 3600

    def texto(self):
        # Representacion legible de la franja.
        return (self._inicio.strftime("%d/%m %H:%M") + "-"
                + self._fin.strftime("%H:%M"))