from abc import ABC, abstractmethod

# Contrato (clase abstracta)
class EstrategiaDescuento(ABC):
    @abstractmethod
    def aplicar(self, precio_base):
        pass
    
# Implementacion
class SinDescuento(EstrategiaDescuento):
    def aplicar(self, precio_base):
        return precio_base

class DescuentoVIP(EstrategiaDescuento):
    def aplicar(self, precio_base):
        return (precio_base * 0.80)
    
class DescuentoEstudiante(EstrategiaDescuento):
    def aplicar(self, precio_base):
        return precio_base * 0.95
    
class DescuentoEmpleado(EstrategiaDescuento):
    def aplicar(self, precio_base):
        return precio_base * 0.75
    
# Creacion de un contexto
class Compra:
    def __init__(self, estrategiaDescuento):
        self.estrategiaDescuento = estrategiaDescuento
        
    def calcularTotal(self, precio):
        return self.estrategiaDescuento.aplicar(precio)
    
def main():
    
    sin_descuento = SinDescuento()
    vip_descuento = DescuentoVIP()
    estudiante_descuento = DescuentoEstudiante()
    empleado_descuento = DescuentoEmpleado()

    compra_1 = Compra(sin_descuento)
    print(compra_1.calcularTotal(100))
    
    compra_2 = Compra(vip_descuento)
    print(compra_2.calcularTotal(1000))
    
    compra_3 = Compra(estudiante_descuento)
    print(compra_3.calcularTotal(10))
    
    compra_4 = Compra(empleado_descuento)
    print(compra_4.calcularTotal(100))

        
main()