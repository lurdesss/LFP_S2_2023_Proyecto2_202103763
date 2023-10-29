class Token():
    def __init__(self, nombre, lexema, fila, columna) -> None:
        self.nombre = nombre
        self.lexema = lexema
        self.fila = fila
        self.columna = columna

    def __str__(self):
        return f'Nombre: {self.nombre}, lexema: {self.lexema}, fila: {self.fila}, columna: {self.columna}'