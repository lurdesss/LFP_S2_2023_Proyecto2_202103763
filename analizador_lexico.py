from error import Error
from token import Token
from comentario import Comentario

class Analizador():
    def __init__(self, texto) -> None:
        self.texto = texto
        self.tokens_reconocidos = []
        self.errores = []
        self.comentarios = []
        self.linea = 1
        self.columna = 1

    # formar un numero entero o decimal
    def tokenize_number(self, input_str, i):
        token = ""
        isDecimal = False
        for char in input_str:
            if char.isdigit():
                token += char
                i += 1
            elif char == "." and not isDecimal:
                token += char
                i += 1
                isDecimal = True
            else:
                break
        if isDecimal:
            return [float(token), i]
        return [int(token), i]


    def tokenize_input(self, input_str):
        i = 0
        self.texto = input_str
        while i < len(input_str):
            char = input_str[i]
            if char.isspace():
                if char == "\n":
                    self.linea += 1
                    self.columna = 1
                elif char == "\t":
                    self.columna += 4
                # si es un espacio
                else:
                    self.columna += 1
                i += 1
            
            elif char == '"':
                string = ""
                j = i + 1
                while j < len(input_str) and input_str[j] != '"':
                    string += input_str[j]
                    j += 1
                if j < len(input_str) and input_str[j] == '"':
                    # Cadena encontrada
                    self.columna += len(string) + 2  # 2 por los caracteres de comillas
                    i = j + 1
                    self.tokens_reconocidos.append(Token('cadena_str', string, self.linea, self.columna))
                else:
                    # Error: cadena no cerrada
                    self.errores.append(Error('cadena_no_cerrada', string, self.linea, self.columna))
                    i = j

            elif input_str[i:i+3] == "'''":
                comment = ""
                j = i + 3
                while j < len(input_str):
                    if input_str[j:j+3] == "'''" and j+3 < len(input_str):
                        # Comentario multilinea encontrado
                        self.columna += len(comment) + 6  # 6 por la longitud de "'''"
                        i = j + 3
                        self.comentarios.append(Comentario('comentario multilinea', comment, self.linea, self.columna))
                        break
                    elif input_str[j] == '\n':
                        comment += input_str[j]
                        self.linea += 1
                        self.columna = 1
                    else:
                        comment += input_str[j]
                    j += 1

            elif char == "#":
                comment = ""
                j = i + 1
                while j < len(input_str) and input_str[j] != "\n":
                    comment += input_str[j]
                    j += 1
                self.columna += len(comment) + 1
                i = j
                self.comentarios.append(Comentario('comentario', comment, self.linea, self.columna))

            elif char == "=":
                self.columna += 1
                i += 1
                self.tokens_reconocidos.append(Token('signo_igual', char, self.linea, self.columna))

            elif char == "[":
                self.columna += 1
                i += 1
                self.tokens_reconocidos.append(Token('corchete_apertura',char, self.linea, self.columna))
            elif char == "]":
                self.columna += 1
                i += 1
                self.tokens_reconocidos.append(Token('corchete_cierre',char, self.linea, self.columna))
            
            elif char == ",":
                self.columna += 1
                i += 1
                self.tokens_reconocidos.append(Token('coma',char, self.linea, self.columna))

            elif char == "{":
                self.columna += 1
                i += 1
                self.tokens_reconocidos.append(Token('llave_apertura',char, self.linea, self.columna))
            elif char == "}":
                self.columna += 1
                i += 1
                self.tokens_reconocidos.append(Token('llave_cierre',char, self.linea, self.columna))
            
            elif char == ";":
                self.columna += 1
                i += 1
                self.tokens_reconocidos.append(Token('punto_coma',char, self.linea, self.columna))

            elif char == "(":
                self.columna += 1
                i += 1
                self.tokens_reconocidos.append(Token('parentesis_apertura',char, self.linea, self.columna))
            
            elif char == ")":
                self.columna += 1
                i += 1
                self.tokens_reconocidos.append(Token('parentesis_cierre',char, self.linea, self.columna))

            elif char.isdigit():
                number, pos = self.tokenize_number(input_str[i:], i)
                self.columna += pos - i
                i = pos
                self.tokens_reconocidos.append(Token('numero',number, self.linea, self.columna))

            elif char.isalpha():
                # Si el carácter es una letra seguida de mas letras, entonces puede ser una palabra reservada o funcion
                keyword = char
                j = i + 1
                while j < len(input_str) and input_str[j].isalpha():
                    keyword += input_str[j]
                    j += 1

                if keyword == "Claves":
                    self.columna += len(keyword)
                    i = j
                    self.tokens_reconocidos.append(Token('clave', keyword, self.linea, self.columna))
                elif keyword == "Registros":
                    self.columna += len(keyword)
                    i = j
                    self.tokens_reconocidos.append(Token('registro', keyword, self.linea, self.columna))
                
                elif keyword == "imprimir":
                    self.columna += len(keyword)
                    i = j
                    self.tokens_reconocidos.append(Token('funcion', 'imprimir', self.linea, self.columna))
                
                elif keyword == "imprimirln":
                    self.columna += len(keyword)
                    i = j
                    self.tokens_reconocidos.append(Token('funcion', 'imprimirln', self.linea, self.columna))
                
                elif keyword == "conteo":
                    self.columna += len(keyword)
                    i = j
                    self.tokens_reconocidos.append(Token('funcion', 'conteo', self.linea, self.columna))
                
                elif keyword == "promedio":
                    self.columna += len(keyword)
                    i = j
                    self.tokens_reconocidos.append(Token('funcion', 'promedio', self.linea, self.columna))
                
                elif keyword == "contarsi":
                    self.columna += len(keyword)
                    i = j
                    self.tokens_reconocidos.append(Token('funcion', 'contarsi', self.linea, self.columna))
                
                elif keyword == "sumar":
                    self.columna += len(keyword)
                    i = j
                    self.tokens_reconocidos.append(Token('funcion', 'sumar', self.linea, self.columna))
                
                elif keyword == "max":
                    self.columna += len(keyword)
                    i = j
                    self.tokens_reconocidos.append(Token('funcion', 'max', self.linea, self.columna))
                
                elif keyword == "min":
                    self.columna += len(keyword)
                    i = j
                    self.tokens_reconocidos.append(Token('funcion', 'min', self.linea, self.columna))
                
                elif keyword == "exportarReporte":
                    self.columna += len(keyword)
                    i = j
                    self.tokens_reconocidos.append(Token('funcion', 'exportarReporte', self.linea, self.columna))

                else:
                    # probable error sintáctico
                    i = j
                    self.errores.append(Error(keyword , 'sintáctico', self.linea, self.columna))

            else:
                # probable error léxi
                i += 1
                self.columna += 1
                self.errores.append(Error(char, 'lexico', self.linea, self.columna))
        
        else:
            print("Análisis terminado")

