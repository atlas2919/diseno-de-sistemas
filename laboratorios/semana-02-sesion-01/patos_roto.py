class ComportamientoVuelo():
    def volar(self):
        raise NotImplementedError

class VuelaConAlas(ComportamientoVuelo):
    def volar(self):
        print("Volando con alas")

class NoVuela(ComportamientoVuelo):
    def volar(self):
        print("No vuelo")


class Pato:
    def __init__(self, comportamiento_vuelo):
        self.comportamiento_vuelo = comportamiento_vuelo

    def nadar(self):
        print("Nadando.")

    def graznar(self):
        print("Cuac!")

    def volar(self):
        self.comportamiento_vuelo.volar()


class PatoSalvaje(Pato):
    def __init__(self):
        vuela_alas = VuelaConAlas()
        super().__init__(vuela_alas)


class PatoDeGoma(Pato):
    def __init__(self):
        no_vuela = NoVuela()
        super().__init__(no_vuela)

    def graznar(self):
        print("Chirrido de goma.")


if __name__ == "__main__":
    salvaje = PatoSalvaje()
    salvaje.nadar()
    salvaje.graznar()
    salvaje.volar()

    print()

    goma = PatoDeGoma()
    goma.nadar()
    goma.graznar()
    goma.volar()  # ahora sí imprime "No vuelo" porque usa el ComportamientoVuelo inyectado