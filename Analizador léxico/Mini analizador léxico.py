import re

class miniLexico:
    def __init__(self, string):
        self.string = string + '$'

    def léxico(self):
        id = ""
        real = ""
        i = 0
        punto = False
        for char in self.string:
            ascii = ord(char)
            if (char=='$'):
                break
            if(ascii==32):
                #print("Hay un espacio \n")
                if(i==0):
                    print("Token no válido")
                    break
                else:
                    i+=1
                    if(len(real)>0):
                        print(real, "es un número real")
                    elif(len(id)>0):
                        print(id, "es un identificador")
                    id = ""
                    real = ""
                    punto = False
            elif (ascii> 64 and ascii < 91) or (ascii>96 and ascii<123):
                if(len(real)>0 or punto ==True):
                    #print("Es letra, pero ya hay real")
                    print("Token no válido")
                    real = ""
                    id = ""
                    break
                id += char
                #print("Es letra", char)
                i+=1
            elif (ascii > 47 and ascii < 58):
                if(len(id)>0):
                    id+=char
                    #print("Es número pero va a id", char)
                    i+=1
                else:
                    real+=char
                    #print("Es número", char)
                    i+=1
            elif (ascii==46):
                if(len(real)>0 and punto==False):
                    #print("Es punto", char)
                    real += char
                    punto=True
                    i+=1
                else:
                    real = ""
                    id = ""
                    punto = False
                    print("Token no válido")
                    break
            else:
                print("Token no válido")
                break
        #print("ID", id)
        #print("Real", real)
        #print("Punto", punto)
        if(len(real)>0):
            print(real, "es un número real")
        elif(len(id)>0):
            print(id, "es un identificador")


cadena = "526a.561"
miniLexico(cadena).léxico()