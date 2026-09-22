import copy

## construir una computadora
class Computadora:
    def __init__(self):
        self.cpu = None
        self.ram = None
        self.disco = None
        self.gpu = None
        self.wifi = None
        
    def mostrar(self):
        print('CPU:', self.cpu)
        print('RAM:', self.ram)
        print('Disco:', self.disco)
        print('GPU:', self.gpu)
        print('Wifi:', 'si tiene wifi' if self.wifi else 'no tiene wifi')
        
    # Clonar la computadora
    def clonar(self):
        return copy.deepcopy(self)
    
    
class ComputadoraBuilder:
    def __init__(self):
        self.computadora = Computadora()
        
    def add_cpu(self, cpu):
        self.computadora.cpu = cpu
        return self
    
    def add_ram(self, ram):
        self.computadora.ram = ram
        return self
        
    def add_disco(self, disco):
        self.computadora.disco = disco
        return self
    
    def add_gpu(self, gpu):
        self.computadora.gpu = gpu
        return self
    
    def add_wifi(self, wifi):
        self.computadora.wifi = wifi
        return self
    
    # creacion del objeto es como un getter
    def build(self):
        return self.computadora
    
def main():
    # constuir una pc_gaming
    pc_builder = ComputadoraBuilder()
    
    # aqui sucede algo mas ...
    
    pc_builder = pc_builder.add_ram(16).add_gpu(18)

    # aqui hay mas codigo...
    
    pc_builder = pc_builder.add_disco(1). add_cpu(20).add_wifi(True)
    
    pc_gaming = pc_builder.build()
    
    pc_gaming.mostrar()
    
    # Clonar el prototipo
    pc_work = pc_gaming.clonar()
    #cambiar especificaciones (oopcional)
    pc_work.ram = 64
    
    pc_work.mostrar()

main()