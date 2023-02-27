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

class Regla:
    def init(self, aux, num, elementos, regla):
        self.aux = aux
        self.num = num
        self.elementos = elementos
        self.regla = regla

listaEstados = []
listaTerminales = []
matrizreglas = list()
auxregl = list()
lisreglas = list()
pila = list()
pilaS = ""

def reglas():
    file = open('compilador.lr', 'r')
    line = file.readlines()
    for l in line:
        l = l.rstrip()
        matrizreglas.append(l.split('\t'))

    for i in range (len(matrizreglas)):
        for j in range(len(matrizreglas[i])):
            matrizreglas[i][j] = int(matrizreglas[i][j])
    file.close()

def auxreglas():
    n = 1
    file = open('rgl.txt', 'r')
    line = file.readlines()
    for l in line:
        l = l.rstrip()
        auxregl.append(l.split('\t'))

    for obj in auxregl:
        obj = Regla(n, int(obj[0]), int(obj[1]), str(obj[2]))
        n+=1
        lisreglas.append(obj)
    file.close()

reglas()
auxreglas()


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

                
cadena = "void menu ( ) { hola = 5 ; } $"
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
        terminal = Terminal(listaDeEstados[i].fuente, listaDeEstados[i].tipo)
        listaTerminales.append(terminal)
    elif(listaDeEstados[i].tipo==1):
        print(listaDeEstados[i].fuente, "es un: entero")
        terminal = Terminal(listaDeEstados[i].fuente, 1)
        listaTerminales.append(terminal)
    elif(listaDeEstados[i].tipo==3):
        print(listaDeEstados[i].fuente, "es un: real")
        terminal = Terminal(listaDeEstados[i].fuente, 2)
        listaTerminales.append(terminal)
    elif(listaDeEstados[i].tipo==4):
        print(listaDeEstados[i].fuente, "es un: identificador")
        terminal = Terminal(listaDeEstados[i].fuente, 0)
        listaTerminales.append(terminal)
    elif(listaDeEstados[i].tipo==6):
        print(listaDeEstados[i].fuente, "es un: string")
        terminal = Terminal(listaDeEstados[i].fuente, 3)
        listaTerminales.append(terminal)
    elif(listaDeEstados[i].tipo==7):
        print(listaDeEstados[i].fuente, "es un: operador Suma")
        terminal = Terminal(listaDeEstados[i].fuente, 5)
        listaTerminales.append(terminal)
    elif(listaDeEstados[i].tipo==8):
        print(listaDeEstados[i].fuente, "es un: operador Multiplicación")
        terminal = Terminal(listaDeEstados[i].fuente, 6)
        listaTerminales.append(terminal)
    elif(listaDeEstados[i].tipo==9 or listaDeEstados[i].tipo==10):
        print(listaDeEstados[i].fuente, "es un: operador Relacional")
        terminal = Terminal(listaDeEstados[i].fuente, 7)
        listaTerminales.append(terminal)
    elif(listaDeEstados[i].tipo==12):
        print(listaDeEstados[i].fuente, "es un: operador OR")
        terminal = Terminal(listaDeEstados[i].fuente, 8)
        listaTerminales.append(terminal)
    elif(listaDeEstados[i].tipo==14):
        print(listaDeEstados[i].fuente, "es un: operador AND")
        terminal = Terminal(listaDeEstados[i].fuente, 9)
        listaTerminales.append(terminal)
    elif(listaDeEstados[i].tipo==15):
        print(listaDeEstados[i].fuente, "es un: operador NOT")
        terminal = Terminal(listaDeEstados[i].fuente, 10)
        listaTerminales.append(terminal)
    elif(listaDeEstados[i].tipo==16):
        print(listaDeEstados[i].fuente, "es un: operador IGUALDAD")
        terminal = Terminal(listaDeEstados[i].fuente, 11)
        listaTerminales.append(terminal)
    elif(listaDeEstados[i].tipo==17):
        print(listaDeEstados[i].fuente, "es un: símbolo igualdad")
        terminal = Terminal(listaDeEstados[i].fuente, 18)
        listaTerminales.append(terminal)
    elif(listaDeEstados[i].tipo==18):
        print(listaDeEstados[i].fuente, "es un: punto y coma")
        terminal = Terminal(listaDeEstados[i].fuente, 12)
        listaTerminales.append(terminal)
    elif(listaDeEstados[i].tipo==19):
        print(listaDeEstados[i].fuente, "es una: coma")
        terminal = Terminal(listaDeEstados[i].fuente, 13)
        listaTerminales.append(terminal)
    elif(listaDeEstados[i].tipo==20):
        print(listaDeEstados[i].fuente, "es un: paréntesis de apertura")
        terminal = Terminal(listaDeEstados[i].fuente, 14)
        listaTerminales.append(terminal)
    elif(listaDeEstados[i].tipo==21):
        print(listaDeEstados[i].fuente, "es un: paréntesis de cierre")
        terminal = Terminal(listaDeEstados[i].fuente, 15)
        listaTerminales.append(terminal)
    elif(listaDeEstados[i].tipo==22):
        print(listaDeEstados[i].fuente, "es una: llave de apertura")
        terminal = Terminal(listaDeEstados[i].fuente, 16)
        listaTerminales.append(terminal)
    elif(listaDeEstados[i].tipo==23):
        print(listaDeEstados[i].fuente, "es una: llave de clausura")
        terminal = Terminal(listaDeEstados[i].fuente, 17)
        listaTerminales.append(terminal)
    elif(listaDeEstados[i].tipo==24):
        print(listaDeEstados[i].fuente, "es un: EOF")
        terminal = Terminal(listaDeEstados[i].fuente, 23)
        listaTerminales.append(terminal)
    elif(listaDeEstados[i].tipo==25):
        print(listaDeEstados[i].fuente, "es palabra reservada: int")
        terminal = Terminal(listaDeEstados[i].fuente, 4)
        listaTerminales.append(terminal)
    elif(listaDeEstados[i].tipo==26):
        print(listaDeEstados[i].fuente, "es palabra reservada: float")
        terminal = Terminal(listaDeEstados[i].fuente, 4)
        listaTerminales.append(terminal)
    elif(listaDeEstados[i].tipo==27):
        print(listaDeEstados[i].fuente, "es palabra reservada: void")
        terminal = Terminal(listaDeEstados[i].fuente, 4)
        listaTerminales.append(terminal)
    elif(listaDeEstados[i].tipo==28):
        print(listaDeEstados[i].fuente, "es palabra reservada: if")
        terminal = Terminal(listaDeEstados[i].fuente, 19)
        listaTerminales.append(terminal)
    elif(listaDeEstados[i].tipo==29):
        print(listaDeEstados[i].fuente, "es palabra reservada: while")
        terminal = Terminal(listaDeEstados[i].fuente, 20)
        listaTerminales.append(terminal)
    elif(listaDeEstados[i].tipo==30):
        print(listaDeEstados[i].fuente, "es palabra reservada: return")
        terminal = Terminal(listaDeEstados[i].fuente, 21)
        listaTerminales.append(terminal)
    elif(listaDeEstados[i].tipo==31):
        print(listaDeEstados[i].fuente, "es palabra reservada: else")
        terminal = Terminal(listaDeEstados[i].fuente, 22)
        listaTerminales.append(terminal) 
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
pila = list()
pilaS = ""
i = 0
tlr1 = list()
data = list()
pila.append(Terminal("$", 23))
pila.append(Estado("", 0))

print("Matriz reglas: ", matrizreglas)
while True:
    obj = listaTerminales[i]
    fila = pila[-1].tipo
    print("Fila: ", fila)
    print("OVJETO", obj.tipo)
    columna = obj.tipo
    print("Columna: ", columna)
    accion = matrizreglas[fila][columna]
    print("ACCION", accion)
    #print("FILA", fila.fuente)
    #print("COLUMNA", columna)

   
    if (accion == 0):
        acc = "NADA"
        print("NADA")
        break
    elif (accion > 0):
        i+=1
        acc = "d"+str(accion)
        pila.append(Terminal(obj.fuente, obj.tipo))
        print("ACC", accion)
        pila.append(Estado(accion))
    elif (accion == -1):
        acc = "r0(acept)"
        print("R0")
        break
    else:
        acc = "r"+str(abs(accion+1))
        for obj2 in lisreglas:
            if (accion == (obj2.num + 1)*-1):
                acc = "r"+str(obj2.num)
                accion = matrizreglas[fila.fuente][obj2.num2]
                if obj2.elem !=0:
                    elim = obj2.elem*2
                    while elim !=0:
                        pila.pop()
                        elim -=1
                    fila = pila[-1]
                    accion = matrizreglas[fila.fuente][obj2.num2]
                    pila.append(obj2)
                    pila.append(Estado(accion))
                else:
                    print("obb", obj.fuente)
                    pila.append(obj2)
                    pila.append(Estado(accion))
                break
    if(i == len(listaTerminales)):
        print("FIN")

for p in pila:
    pilaS += str(p.fuente)
    data.append([pilaS, obj.fuente, acc])
    pilaS = ""
    
print(tabulate(data, headers=["Pila", "Entrada", "Salida"]))


        





