############## SISTEMA DE COMPRA EN LINEA ######################
class Inventario:
    def verificar(self, producto):
        print(f'Verificando el stock de {producto}')
        return True
        
class Pago:
    def procesar(self, monto):
        print(f'Procesando pago: {monto}')
        return True
    
class Envio:
    def crear_envio(self, producto):
        print(f'Preparando el envio del: {producto}')
        
class Notificacion:
    def enviar(self, correo, mensaje):
        print(f'Enviando correo a {correo} vía Gmail...')
        print(f'Mensaje: {mensaje}')
        return True
        
## Fachada
class TiendaFacade:
    def __init__(self):
        self.inventario = Inventario()
        self.pago = Pago()
        self.envio = Envio()
        self.notificacion = Notificacion()

    def comprar(self, producto, precio, correo):
        if not self.inventario.verificar(producto):
            print('No hay stock')
            return

        if not self.pago.procesar(precio):
            print('Fallo el pago')
            return

        self.envio.crear_envio(producto)

        mensaje = f'Tu compra de {producto} por ${precio} fue confirmada y ya está en camino.'
        self.notificacion.enviar(correo, mensaje)

        print('Compra completada')
        
def main():
    
    # Instaciar la fachada
    tienda = TiendaFacade()
    
    # Hacer la compra
    tienda.comprar('Laptop', 1500, 'cliente@gmail.com')
        
main()
