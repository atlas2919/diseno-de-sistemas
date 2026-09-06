# Estados posibles de una reserva.

from enum import Enum

class EstadoReserva(Enum):
    CONFIRMADA = "confirmada"
    CANCELADA = "cancelada"
    NO_SHOW = "no-show"
    DESPLAZADA = "desplazada"

    def __str__(self) -> str:
        return self.value