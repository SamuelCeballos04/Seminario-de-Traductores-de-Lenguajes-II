class Lexico:
    def __init__(self, string):
        self.string = string + '$'

    def léxico(self):
        estado = 0
        aux = ""
        i = 0
        #print("String a analizar", cadena)
        #print("Tamaño de cadena", len(cadena))
        for char in self.string:
            ascii = ord(char)
            if (char == '$'):
                break
            elif (estado == 0):
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
        #print("Caracter", aux)
        return estado, aux

                
cadena = "12.598"
estado, stringFinal = Lexico(cadena).léxico()
#print("Estado", estado, "Cadena", stringFinal)
if(estado==1):
    print(stringFinal, "es un: entero")
elif(estado==3):
    print(stringFinal, "es un: real")
elif(estado==4):
    print(stringFinal, "es un: identificador")
elif(estado==6):
    print(stringFinal, "es un: string")
elif(estado==7):
    print(stringFinal, "es un: operador Suma")


