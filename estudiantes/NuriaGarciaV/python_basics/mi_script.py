# Definimos una clase
class Estudiante:
    def __init__(self, nombre, nota):
        self.nombre = nombre
        self.nota = nota

    def mostrar_resultado(self):
        if self.nota >= 60:
            print(f"{self.nombre} aprobó con nota {self.nota}")
        else:
            print(f"{self.nombre} reprobó con nota {self.nota}")

# Definimos una función
def evaluar_estudiante():
    nombre = input("Ingresa el nombre del estudiante: ")
    nota = int(input("Ingresa la nota: "))

    estudiante = Estudiante(nombre, nota)
    estudiante.mostrar_resultado()

# Ejecutamos el programa
evaluar_estudiante()
