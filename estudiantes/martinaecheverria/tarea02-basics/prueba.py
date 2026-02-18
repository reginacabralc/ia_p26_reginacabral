class CalculadoraEspacial:
    """
    Esta clase representa una calculadora básica para misiones espaciales.
    Permite sumar combustible, calcular distancias
    y verificar si hay suficiente combustible para llegar a Marte.
    """

    def __init__(self, combustible_inicial=0):
        """
        Constructor de la clase.
        Inicializa la cantidad de combustible disponible.
        """
        self.combustible = combustible_inicial

    def sumar_combustible(self, cantidad):
        """
        Suma una cantidad de combustible al total disponible.
        """
        self.combustible += cantidad
        return self.combustible

    def calcular_distancia(self, velocidad, tiempo):
        """
        Calcula la distancia recorrida usando la fórmula:
        distancia = velocidad * tiempo
        """
        return velocidad * tiempo

    def puede_llegar_a_marte(self):
        """
        Decide si hay suficiente combustible para llegar a Marte.
        Se necesitan al menos 100 unidades de combustible.
        """
        if self.combustible >= 100:
            return True
        else:
            return False


# Ejemplo de uso
calculadora = CalculadoraEspacial(50)
calculadora.sumar_combustible(60)

if calculadora.puede_llegar_a_marte():
    print("¡Tenemos suficiente combustible para llegar a Marte!")
else:
    print("No hay suficiente combustible para llegar a Marte.")

