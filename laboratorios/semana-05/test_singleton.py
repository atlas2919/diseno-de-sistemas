from singleton import GestorDeConfiguracion, reserva_permitida

# Las pruebas tienen que ir en funciones
def test_rechaza_reserva():
    config = GestorDeConfiguracion.obtener_objeto()
    config.modo_mantenimiento = True
    
    ## assert sirve para hacer preguntas
    assert reserva_permitida(config) is False
    
def test_reserva_aceptada():
    config = GestorDeConfiguracion.obtener_objeto()
    config.modo_mantenimiento = False
    assert reserva_permitida(config) is True
    
## Falla porque el primer test modifica el objeto compartido y no lo devuelve al estado original
