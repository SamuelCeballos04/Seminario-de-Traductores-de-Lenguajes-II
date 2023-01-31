from tabulate import tabulate 

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
                    listaEstados.append(estado)
                    listaTokens.append(aux)
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
                    listaEstados.append(estado)
                    listaTokens.append(aux)
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
                    listaEstados.append(25)
                    listaTokens.append(aux)
                    estado = 0
                    aux = ""
                elif(aux == "float"):
                    listaEstados.append(26)
                    listaTokens.append(aux)
                    estado = 0
                    aux = ""
                elif (aux == "void"):
                    listaEstados.append(27)
                    listaTokens.append(aux)
                    estado = 0
                    aux = ""
                elif(aux == "if"):
                    listaEstados.append(28)
                    listaTokens.append(aux)
                    estado = 0
                    aux = ""
                elif(aux == "while"):
                    listaEstados.append(29)
                    listaTokens.append(aux)
                    estado = 0
                    aux = ""
                elif (aux == "return"):
                    listaEstados.append(30)
                    listaTokens.append(aux)
                    estado = 0
                    aux = ""
                elif(aux == "else"):
                    listaEstados.append(31)
                    listaTokens.append(aux)
                    estado = 0
                    aux = ""
                elif (ascii==32):
                    listaEstados.append(estado)
                    listaTokens.append(aux)
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
                    listaEstados.append(estado)
                    listaTokens.append(aux)
                    aux = ""
                    estado = 0
                else:
                    print("Algo salió mal")
                    break
            elif(estado == 7):
                if (ascii==32):
                    listaEstados.append(estado)
                    listaTokens.append(aux)
                    aux = ""
                    estado = 0
                else:
                    print("Algo salió mal")
                    break
            elif(estado == 8):
                if (ascii==32):
                    listaEstados.append(estado)
                    listaTokens.append(aux)
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
                    listaEstados.append(estado)
                    listaTokens.append(aux)
                    aux = ""
                    estado = 0
                else:
                    print("Algo salió mal")
                    break
            elif(estado == 10):                
                if(ascii==32):
                    listaEstados.append(estado)
                    listaTokens.append(aux)
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
                    listaEstados.append(estado)
                    listaTokens.append(aux)
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
                    listaEstados.append(estado)
                    listaTokens.append(aux)
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
                    listaEstados.append(estado)
                    listaTokens.append(aux)
                    aux = ""
                    estado = 0
                else:
                    print("Algo salió mal")
                    break       
            elif(estado == 16):                
                if(ascii==32):
                    listaEstados.append(estado)
                    listaTokens.append(aux)
                    aux = ""
                    estado = 0
                else:
                    print("Algo salió mal")
                    break     
            elif(estado == 17):                
                if(ascii==32):
                    listaEstados.append(estado)
                    listaTokens.append(aux)
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
                    listaEstados.append(estado)
                    listaTokens.append(aux)
                    aux = ""
                    estado = 0
                else:
                    print("Algo salió mal")
                    break 
            elif(estado == 19):                
                if(ascii==32):
                    listaEstados.append(estado)
                    listaTokens.append(aux)
                    aux = ""
                    estado = 0
                else:
                    print("Algo salió mal")
                    break  
            elif(estado == 20):                
                if(ascii==32):
                    listaEstados.append(estado)
                    listaTokens.append(aux)
                    aux = ""
                    estado = 0
                else:
                    print("Algo salió mal")
                    break  
            elif(estado == 21):                
                if(ascii==32):
                    listaEstados.append(estado)
                    listaTokens.append(aux)
                    aux = ""
                    estado = 0
                else:
                    print("Algo salió mal")
                    break    
            elif(estado == 22):                
                if(ascii==32):
                    listaEstados.append(estado)
                    listaTokens.append(aux)
                    aux = ""
                    estado = 0
                else:
                    print("Algo salió mal")
                    break  
            elif(estado == 23):                
                if(ascii==32):
                    listaEstados.append(estado)
                    listaTokens.append(aux)
                    aux = ""
                    estado = 0
                else:
                    print("Algo salió mal")
                    break     
            elif(estado == 24):                
                if(ascii==32):
                    listaEstados.append(estado)
                    listaTokens.append(aux)
                    aux = ""
                    estado = 0
                else:
                    print("Algo salió mal")
                    break
        listaEstados.append(estado)
        listaTokens.append(aux)
        #print("Caracter", aux)
        print("Lista de tokens: ", listaTokens)
        print("Lista de estados: ", listaEstados)
        return listaTokens, listaEstados

                
cadena = "a + b + c + d + e + f $"
estados = []
tokens = []
tokens, estados = Lexico(cadena).léxico()
#print("Estado", estado, "Cadena", stringFinal)
i = 0
valoresTokens = []
while i < len(estados):
    if(estados[i]==0):
        print(tokens[i], "no es válido")
        valoresTokens.append("int")
    elif(estados[i]==1):
        print(tokens[i], "es un: entero")
    elif(estados[i]==3):
        print(tokens[i], "es un: real")
    elif(estados[i]==4):
        print(tokens[i], "es un: identificador")
        valoresTokens.append("id")
    elif(estados[i]==6):
        print(tokens[i], "es un: string")
    elif(estados[i]==7):
        print(tokens[i], "es un: operador Suma")
        valoresTokens.append("+")
    elif(estados[i]==8):
        print(tokens[i], "es un: operador Multiplicación")
    elif(estados[i]==9 or estados[i]==10):
        print(tokens[i], "es un: operador Relacional")
    elif(estados[i]==12):
        print(tokens[i], "es un: operador OR")
    elif(estados[i]==14):
        print(tokens[i], "es un: operador AND")
    elif(estados[i]==15):
        print(tokens[i], "es un: operador NOT")
    elif(estados[i]==16):
        print(tokens[i], "es un: operador IGUALDAD")
    elif(estados[i]==17):
        print(tokens[i], "es un: símbolo igualdad")
    elif(estados[i]==18):
        print(tokens[i], "es un: punto y coma")
    elif(estados[i]==19):
        print(tokens[i], "es una: coma")
    elif(estados[i]==20):
        print(tokens[i], "es un: paréntesis de apertura")
    elif(estados[i]==21):
        print(tokens[i], "es un: paréntesis de cierre")
    elif(estados[i]==22):
        print(tokens[i], "es una: llave de apertura")
    elif(estados[i]==23):
        print(tokens[i], "es una: llave de clausura")
    elif(estados[i]==24):
        print(tokens[i], "es un: EOF")
        valoresTokens.append("$")
    elif(estados[i]==25):
        print(tokens[i], "es palabra reservada: int")
    elif(estados[i]==26):
        print(tokens[i], "es palabra reservada: float")
    elif(estados[i]==27):
        print(tokens[i], "es palabra reservada: void")
    elif(estados[i]==28):
        print(tokens[i], "es palabra reservada: if")
    elif(estados[i]==29):
        print(tokens[i], "es palabra reservada: while")
    elif(estados[i]==30):
        print(tokens[i], "es palabra reservada: return")
    elif(estados[i]==31):
        print(tokens[i], "es palabra reservada: else")    
    i+=1

print("Lista de tokens: ", valoresTokens)

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
pila.append("$")
pila.append("0")
fila = 0
columna = 0
datosFin = []
stringPila = "$0"
i = 0


for objeto in valoresTokens:
    if objeto == "id":
        fila = int(pila[-1])
        columna = 0
        salida = LR2[fila][columna]
        stringPila += tokens[i]
        stringPila += str(salida)
        datosSalida = "d" + str(salida)
        pila.append(tokens[i])
        pila.append(salida)
        datosFin.append([stringPila, tokens[i], datosSalida])
        datosSalida = ""
    elif objeto == "+":
        fila = int(pila[-1])
        columna = 1
        salida = LR2[fila][columna]
        stringPila += tokens[i]
        stringPila += str(salida)
        datosSalida = "d" + str(salida)
        pila.append(tokens[i])
        pila.append(salida)
        datosFin.append([stringPila, tokens[i], datosSalida])
        datosSalida = ""
    elif objeto == "$":
        fila = int(pila[-1])
        columna = 2
        salida = LR2[fila][columna] 
        stringPila = "$0"
        stringPila += "E"
        stringPila += str(salida+5)
        datosSalida = "r" + str(salida+5)
        del pila[2:]
        pila.append("E")
        pila.append("1")
        datosFin.append([stringPila, tokens[i], datosSalida])
        datosSalida = ""
        fila = int(pila[-1])
        columna = 2
        salida = LR1[fila][columna]
        if salida == -1:
            print("Aceptada")
    print("Lista sobre la que se itera: ", valoresTokens)

    i+=1    

print("String Pila: ", stringPila)
print("Datos finales: ", datosFin)
print("Pila", pila)


        





