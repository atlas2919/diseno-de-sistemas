# Politicas de prioridad.

from abc import ABC, abstractmethod
from datetime import time

from franja_horaria import FranjaHoraria


class ReglaPrioridad(ABC):
    @abstractmethod
    def aplica(self, franja: FranjaHoraria) -> bool:
        """Indica si la prioridad procede para la franja indicada."""
    @abstractmethod
    def descripcion(self) -> str:
        """Texto legible de la politica, para efectos de trazabilidad."""


class PrioridadEquipoOficial(ReglaPrioridad):
    def __init__(self, hora_limite: time = time(18, 0)) -> None:
        self._hora_limite = hora_limite

    def aplica(self, franja: FranjaHoraria) -> bool:
        return franja.inicia_antes_de(self._hora_limite)

    def descripcion(self) -> str:
        return f"prioridad antes de las {self._hora_limite.strftime('%H:%M')}"


class SinPrioridad(ReglaPrioridad):
    def aplica(self, franja: FranjaHoraria) -> bool:
        return False

    def descripcion(self) -> str:
        return "sin prioridad"