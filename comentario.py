class Comentario():
    def __init__(self, tipo, estructura, fila, columna) -> None:
        self.tipo = tipo
        self.estructura = estructura
        self.fila = fila
        self.columna = columna

    def __str__(self):
        return f'Tipo: {self.tipo}, estructura: {self.estructura}, fila: {self.fila}, columna: {self.columna}'