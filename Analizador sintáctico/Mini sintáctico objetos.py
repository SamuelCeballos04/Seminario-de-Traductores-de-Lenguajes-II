from tabulate import tabulate 

class ElementoPila:
    def __init__(self, fuente, tipo):
        self.fuente = fuente
        self.tipo = tipo

class Terminal(ElementoPila):
    def __init__(self, fuente, tipo):
        super().__init__(fuente, tipo)

class NoTerminal(ElementoPila):
    def __init__(self, fuente, tipo):
        super().__init__(fuente, tipo)

class Estado(ElementoPila):
    def __init__(self, fuente, tipo):
        super().__init__(fuente, tipo)

listaEstados = []
listaTerminales = []

class Lexico:
    def __init__(self, string):
        self.string = string + '$'

    def léxico(self):
        estado = 0
        aux = ""
        i = 0
        listaTokens = []
        listaEstados = []

        #print("String a analizar", cadena)
        #print("Tamaño de cadena", len(cadena))
        for char in self.string:
            ascii = ord(char)
            if (estado == 0):
                if(ascii > 47 and ascii < 58):
                    #print("Es número")
                    estado = 1
                    aux+=char
                elif (ascii> 64 and ascii < 91) or (ascii>96 and ascii<123):
                    #print("Es letra")
                    estado = 4
                    aux+=char
                elif(ascii == 39):
                    estado = 5
                    aux+=char
                elif(ascii == 43 or ascii == 45):
                    estado = 7
                    aux+=char
                elif(ascii == 42 or ascii == 47):
                    estado = 8
                    aux+=char
                elif(ascii == 60 or ascii == 62):
                    estado = 9
                    aux+=char
                elif(ascii == 124):
                    estado = 11
                    aux+=char
                elif(ascii == 38):
                    estado = 13
                    aux+=char
                elif(ascii == 33):
                    estado = 15
                    aux+=char
                elif(ascii == 61):
                    estado = 17
                    aux+=char
                elif(ascii == 59):
                    estado = 18
                    aux+=char
                elif(ascii == 44):
                    estado = 19
                    aux+=char
                elif(ascii == 40):
                    estado = 20
                    aux+=char
                elif(ascii == 41):
                    estado = 21
                    aux+=char
                elif(ascii == 123):
                    estado = 22
                    aux+=char
                elif(ascii == 125):
                    estado = 23
                    aux+=char
                elif(ascii == 36):
                    estado = 24
                    aux+=char
                else:
                    print("Algo salió mal")
                    break
            elif (estado==1):
                if(ascii > 47 and ascii < 58):
                    #print("Es número")
                    estado = 1
                    aux+=char
                elif(ascii == 46):
                    #print("Es punto")
                    estado = 2
                    aux+=char
                elif (ascii==32):
                    # listaEstados.append(estado)
                    # listaTokens.append(aux)
                    state = Estado(aux, estado)
                    listaEstados.append(state)
                    aux = ""
                    estado = 0
                else:
                    print("Algo salió mal")
                    break
            elif (estado==2):
                if(ascii > 47 and ascii < 58):
                    #print("Es número")
                    estado = 3
                    aux+=char
                else:
                    print("Algo salió mal")
                    break
            elif (estado==3):
                if(ascii > 47 and ascii < 58):
                    #print("Es número")
                    estado = 3
                    aux+=char
                elif (ascii==32):
                    # listaEstados.append(estado)
                    # listaTokens.append(aux)
                    state = Estado(aux, estado)
                    listaEstados.append(state)
                    aux = ""
                    estado = 0
                else:
                    print("Algo salió mal")
                    break
            elif(estado==4):
                if(ascii > 47 and ascii < 58):
                    #print("Es número")
                    estado = 4
                    aux+=char
                elif (ascii> 64 and ascii < 91) or (ascii>96 and ascii<123):
                    #print("Es letra")
                    estado = 4
                    aux+=char
                elif(aux == 'int'):
                    # listaEstados.append(25)
                    # listaTokens.append(aux)
                    state = Estado(aux, 25)
                    listaEstados.append(state)
                    estado = 0
                    aux = ""
                elif(aux == "float"):
                    # listaEstados.append(26)
                    # listaTokens.append(aux)
                    state = Estado(aux, 26)
                    listaEstados.append(state)
                    estado = 0
                    aux = ""
                elif (aux == "void"):
                    # listaEstados.append(27)
                    # listaTokens.append(aux)
                    state = Estado(aux, 27)
                    listaEstados.append(state)
                    estado = 0
                    aux = ""
                elif(aux == "if"):
                    # listaEstados.append(28)
                    # listaTokens.append(aux)
                    state = Estado(aux, 28)
                    listaEstados.append(state)
                    estado = 0
                    aux = ""
                elif(aux == "while"):
                    # listaEstados.append(29)
                    # listaTokens.append(aux)
                    state = Estado(aux, 29)
                    listaEstados.append(state)
                    estado = 0
                    aux = ""
                elif (aux == "return"):
                    # listaEstados.append(30)
                    # listaTokens.append(aux)
                    state = Estado(aux, 30)
                    listaEstados.append(state)
                    estado = 0
                    aux = ""
                elif(aux == "else"):
                    # listaEstados.append(31)
                    # listaTokens.append(aux)
                    state = Estado(aux, 31)
                    listaEstados.append(state)
                    estado = 0
                    aux = ""
                elif (ascii==32):
                    # listaEstados.append(estado)
                    # listaTokens.append(aux)
                    state = Estado(aux, estado)
                    listaEstados.append(state)
                    aux = ""
                    estado = 0
                else:
                    print("Algo salió mal")
                    break
            elif(estado==5):
                if(ascii > 47 and ascii < 58):
                    #print("Es número")
                    estado = 5
                    aux+=char
                elif (ascii> 64 and ascii < 91) or (ascii>96 and ascii<123):
                    #print("Es letra")
                    estado = 5
                    aux+=char
                elif(ascii == 32):
                    estado = 5
                    aux+=char
                elif(ascii == 39):
                    estado = 6
                    aux+=char
                else:
                    print("Algo salió mal")
                    break
            elif(estado == 6):
                if (ascii==32):
                    # listaEstados.append(estado)
                    # listaTokens.append(aux)
                    state = Estado(aux, estado)
                    listaEstados.append(state)
                    aux = ""
                    estado = 0
                else:
                    print("Algo salió mal")
                    break
            elif(estado == 7):
                if (ascii==32):
                    # listaEstados.append(estado)
                    # listaTokens.append(aux)
                    state = Estado(aux, estado)
                    listaEstados.append(state)
                    aux = ""
                    estado = 0
                else:
                    print("Algo salió mal")
                    break
            elif(estado == 8):
                if (ascii==32):
                    # listaEstados.append(estado)
                    # listaTokens.append(aux)
                    state = Estado(aux, estado)
                    listaEstados.append(state)
                    aux = ""
                    estado = 0
                else:
                    print("Algo salió mal")
                    break
            elif(estado == 9):                
                if (ascii==61):
                    estado = 10
                    aux+=char
                elif(ascii==32):
                    # listaEstados.append(estado)
                    # listaTokens.append(aux)
                    state = Estado(aux, estado)
                    listaEstados.append(state)
                    aux = ""
                    estado = 0
                else:
                    print("Algo salió mal")
                    break
            elif(estado == 10):                
                if(ascii==32):
                    # listaEstados.append(estado)
                    # listaTokens.append(aux)
                    state = Estado(aux, estado)
                    listaEstados.append(state)
                    aux = ""
                    estado = 0
                else:
                    print("Algo salió mal")
                    break    
            elif(estado == 11):                
                if(ascii==124):
                    estado = 12
                    aux+=char
                else:
                    print("Algo salió mal")
                    break  
            elif(estado == 12):                
                if(ascii==32):
                    # listaEstados.append(estado)
                    # listaTokens.append(aux)
                    state = Estado(aux, estado)
                    listaEstados.append(state)
                    aux = ""
                    estado = 0
                else:
                    print("Algo salió mal")
                    break 
            elif(estado == 13):                
                if(ascii==38):
                    estado = 14
                    aux+=char
                else:
                    print("Algo salió mal")
                    break  
            elif(estado == 14):                
                if(ascii==32):
                    # listaEstados.append(estado)
                    # listaTokens.append(aux)
                    state = Estado(aux, estado)
                    listaEstados.append(state)
                    aux = ""
                    estado = 0
                else:
                    print("Algo salió mal")
                    break      
            elif(estado == 15):                
                if(ascii == 61):
                    estado = 16
                    aux+=char
                elif(ascii==32):
                    # listaEstados.append(estado)
                    # listaTokens.append(aux)
                    state = Estado(aux, estado)
                    listaEstados.append(state)
                    aux = ""
                    estado = 0
                else:
                    print("Algo salió mal")
                    break       
            elif(estado == 16):                
                if(ascii==32):
                    # listaEstados.append(estado)
                    # listaTokens.append(aux)
                    state = Estado(aux, estado)
                    listaEstados.append(state)
                    aux = ""
                    estado = 0
                else:
                    print("Algo salió mal")
                    break     
            elif(estado == 17):                
                if(ascii==32):
                    # listaEstados.append(estado)
                    # listaTokens.append(aux)
                    state = Estado(aux, estado)
                    listaEstados.append(state)
                    aux = ""
                    estado = 0
                elif(ascii == 61):
                    estado = 16
                    aux+=char
                else:
                    print("Algo salió mal")
                    break      
            elif(estado == 18):                
                if(ascii==32):
                    # listaEstados.append(estado)
                    # listaTokens.append(aux)
                    state = Estado(aux, estado)
                    listaEstados.append(state)
                    aux = ""
                    estado = 0
                else:
                    print("Algo salió mal")
                    break 
            elif(estado == 19):                
                if(ascii==32):
                    # listaEstados.append(estado)
                    # listaTokens.append(aux)
                    state = Estado(aux, estado)
                    listaEstados.append(state)
                    aux = ""
                    estado = 0
                else:
                    print("Algo salió mal")
                    break  
            elif(estado == 20):                
                if(ascii==32):
                    # listaEstados.append(estado)
                    # listaTokens.append(aux)
                    state = Estado(aux, estado)
                    listaEstados.append(state)
                    aux = ""
                    estado = 0
                else:
                    print("Algo salió mal")
                    break  
            elif(estado == 21):                
                if(ascii==32):
                    # listaEstados.append(estado)
                    # listaTokens.append(aux)
                    state = Estado(aux, estado)
                    listaEstados.append(state)
                    aux = ""
                    estado = 0
                else:
                    print("Algo salió mal")
                    break    
            elif(estado == 22):                
                if(ascii==32):
                    # listaEstados.append(estado)
                    # listaTokens.append(aux)
                    state = Estado(aux, estado)
                    listaEstados.append(state)
                    aux = ""
                    estado = 0
                else:
                    print("Algo salió mal")
                    break  
            elif(estado == 23):                
                if(ascii==32):
                    # listaEstados.append(estado)
                    # listaTokens.append(aux)
                    state = Estado(aux, estado)
                    listaEstados.append(state)
                    aux = ""
                    estado = 0
                else:
                    print("Algo salió mal")
                    break     
            elif(estado == 24):                
                if(ascii==32):
                    # listaEstados.append(estado)
                    # listaTokens.append(aux)
                    state = Estado(aux, estado)
                    listaEstados.append(state)
                    aux = ""
                    estado = 0
                else:
                    print("Algo salió mal")
                    break
        # listaEstados.append(estado)
        # listaTokens.append(aux)
        print("Aux:", aux)
        state = Estado(aux, estado)
        listaEstados.append(state)
        #print("Caracter", aux)
        # print("Lista de tokens: ", listaTokens)
        # print("Lista de estados: ", listaEstados)
        return listaEstados

                
cadena = "hola + mundo $"
estados = []
tokens = []
# listaDeEstados = []
listaDeEstados = Lexico(cadena).léxico()
#print("Estado", estado, "Cadena", stringFinal)
i = 0
valoresTokens = []
print("Len lista de estados: ", len(listaDeEstados))
while i < len(listaDeEstados):
    print("Tipo: ", listaDeEstados[i].tipo)
    print("Fuente: ", listaDeEstados[i].fuente)
    if(listaDeEstados[i].tipo==0):
        print(listaDeEstados[i].fuente, "no es válido")
        terminal = Terminal(listaDeEstados[i].fuente, "no válido")
        listaTerminales.append(terminal)
    elif(listaDeEstados[i].tipo==1):
        print(listaDeEstados[i].fuente, "es un: entero")
    elif(listaDeEstados[i].tipo==3):
        print(listaDeEstados[i].fuente, "es un: real")
    elif(listaDeEstados[i].tipo==4):
        print(listaDeEstados[i].fuente, "es un: identificador")
        # valoresTokens.append("id")
        terminal = Terminal(listaDeEstados[i].fuente, "id")
        listaTerminales.append(terminal)
    elif(listaDeEstados[i].tipo==6):
        print(listaDeEstados[i].fuente, "es un: string")
    elif(listaDeEstados[i].tipo==7):
        print(listaDeEstados[i].fuente, "es un: operador Suma")
        # valoresTokens.append("+")
        terminal = Terminal(listaDeEstados[i].fuente, "+")
        listaTerminales.append(terminal)
    elif(listaDeEstados[i].tipo==8):
        print(listaDeEstados[i].fuente, "es un: operador Multiplicación")
    elif(listaDeEstados[i].tipo==9 or listaDeEstados[i].tipo==10):
        print(listaDeEstados[i].fuente, "es un: operador Relacional")
    elif(listaDeEstados[i].tipo==12):
        print(listaDeEstados[i].fuente, "es un: operador OR")
    elif(listaDeEstados[i].tipo==14):
        print(listaDeEstados[i].fuente, "es un: operador AND")
    elif(listaDeEstados[i].tipo==15):
        print(listaDeEstados[i].fuente, "es un: operador NOT")
    elif(listaDeEstados[i].tipo==16):
        print(listaDeEstados[i].fuente, "es un: operador IGUALDAD")
    elif(listaDeEstados[i].tipo==17):
        print(listaDeEstados[i].fuente, "es un: símbolo igualdad")
    elif(listaDeEstados[i].tipo==18):
        print(listaDeEstados[i].fuente, "es un: punto y coma")
    elif(listaDeEstados[i].tipo==19):
        print(listaDeEstados[i].fuente, "es una: coma")
    elif(listaDeEstados[i].tipo==20):
        print(listaDeEstados[i].fuente, "es un: paréntesis de apertura")
    elif(listaDeEstados[i].tipo==21):
        print(listaDeEstados[i].fuente, "es un: paréntesis de cierre")
    elif(listaDeEstados[i].tipo==22):
        print(listaDeEstados[i].fuente, "es una: llave de apertura")
    elif(listaDeEstados[i].tipo==23):
        print(listaDeEstados[i].fuente, "es una: llave de clausura")
    elif(listaDeEstados[i].tipo==24):
        print(listaDeEstados[i].fuente, "es un: EOF")
        # valoresTokens.append("$")
        terminal = Terminal(listaDeEstados[i].fuente, "$")
        listaTerminales.append(terminal)
    elif(listaDeEstados[i].tipo==25):
        print(listaDeEstados[i].fuente, "es palabra reservada: int")
    elif(listaDeEstados[i].tipo==26):
        print(listaDeEstados[i].fuente, "es palabra reservada: float")
    elif(listaDeEstados[i].tipo==27):
        print(listaDeEstados[i].fuente, "es palabra reservada: void")
    elif(listaDeEstados[i].tipo==28):
        print(listaDeEstados[i].fuente, "es palabra reservada: if")
    elif(listaDeEstados[i].tipo==29):
        print(listaDeEstados[i].fuente, "es palabra reservada: while")
    elif(listaDeEstados[i].tipo==30):
        print(listaDeEstados[i].fuente, "es palabra reservada: return")
    elif(listaDeEstados[i].tipo==31):
        print(listaDeEstados[i].fuente, "es palabra reservada: else")    
    i+=1

LR1 = [[2,0,0,1],
        [0,0,-1,0],
        [0,3,0,0],
        [4,0,0,0],
        [0,0,-2,0]]

LR2 = [[2,0,0,1],
        [0,0,-1,0],
        [0,3,-3,0],
        [2,0,0,4],
        [0,0,-2,0]]

pila = []
terminalPila = Terminal("$", "$")
pila.append(terminalPila)
terminalPila = Terminal("0", "0")
pila.append(terminalPila)
fila = 0
columna = 0
datosFin = []
stringPila = "$0"
i = 0



for objeto in listaTerminales:
    if objeto.tipo == "id":
        fila = int(pila[-1].tipo)
        columna = 0
        salida = LR1[fila][columna]
        # stringPila += tokens[i]
        stringPila += objeto.fuente
        stringPila += str(salida)
        datosSalida = "d" + str(salida)
        terminal = Terminal(objeto.fuente, salida)
        pila.append(terminal)
        datosFin.append([stringPila, objeto.fuente, datosSalida])
        datosSalida = ""
    elif objeto.tipo == "+":
        fila = int(pila[-1].tipo)
        columna = 1
        salida = LR1[fila][columna]
        stringPila += objeto.fuente
        stringPila += str(salida)
        datosSalida = "d" + str(salida)
        terminal = Terminal(objeto.fuente, salida)
        pila.append(terminal)
        datosFin.append([stringPila, objeto.fuente, datosSalida])
        datosSalida = ""
    elif objeto.tipo == "$":
        fila = int(pila[-1].tipo)
        columna = 2
        salida = LR1[fila][columna] 
        stringPila = "$0"
        stringPila += "E"
        stringPila += str(salida+5)
        datosSalida = "r" + str(salida+5)
        del pila[2:]
        terminal = Terminal("E", "1")
        pila.append(terminal)
        datosFin.append([stringPila, objeto.fuente, datosSalida])
        datosSalida = ""
        fila = int(pila[-1].tipo)
        columna = 2
        salida = LR1[fila][columna]
        if salida == -1:
            print("La cadena es aceptada")
    i+=1    

print(tabulate(datosFin, headers=["Pila", "Entrada", "Salida"]))


        





