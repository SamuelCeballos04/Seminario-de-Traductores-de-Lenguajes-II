from asyncio.windows_events import NULL
from dataclasses import dataclass
from genericpath import exists
import numpy as np
from anytree import Node, RenderTree
#from generacion import traduccion_sasm
#from clases import *
from tabulate import tabulate 
import re

class Variables:
    def __init__(self, cad, contexto):
        self.cad = cad
        self.contexto = contexto
    def __repr__(self):
        objeto = ("Variable: "+str(self.cad)+" Contexto: "+str(self.context))
        return objeto

class Retorno:
    def __init__(self, cad, tipo, context):
        self.cad = cad
        self.tipo = tipo
        self.context = context
    def __repr__(self):
        objeto = ("Valor/Variable: "+str(self.cad)+ " Tipo: "+str(self.tipo)+ " Contexto: "+str(self.context))
        return objeto
        
class Nodo:
    def __init__(self, data):
        self.data = data
        self.contadordefinicion =0

class Seg_Parametros(Nodo):
    def __init__(self, data, id, tipo):
        Nodo.__init__(self, data)
        self.id = id
        self.tipo = tipo
    def __repr__(self):
        objeto = ('Parametros' '\n'+ ' Tipo: '+str(self.data)+' Id: '+str(self.id) + ' Funcion: ' + str(self.tipo))
        return objeto

class Regla:
    def __init__(self, aux, num, elementos, regla):
        self.aux = aux
        self.num = num
        self.elementos = elementos
        self.regla = regla


class Plantilla_Pila:
    def __init__(self, cadena, tipo, pos):
        self.cad = cadena
        self.tipo = tipo
        self.pos = pos

    def __repr__(self):
        return str(self.__dict__)

class Terminal(Plantilla_Pila):
    def __init__(self, cadena, tipo, pos):
        Plantilla_Pila.__init__(self, cadena, tipo, pos)

class No_Terminal(Plantilla_Pila):
    def __init__(self, cadena, tipo, pos):
        Plantilla_Pila.__init__(self, cadena, tipo, pos)

class Estado(Plantilla_Pila):
    def __init__(self, cadena, tipo, pos, estado):
        Plantilla_Pila.__init__(self, cadena, tipo, pos)
        self.estado = estado

class refer():
    def __init__(self, var, contexto, pos):
        self.var = var
        self.contexto = contexto
        self.pos = pos

list_ref = list()
globals()['cont']=''
globals()['prim']=0

class traduccion_sasm():
    def __init__(self):

        self.codigo = list()
        self.posicionvar = 4
        self.comienzo = 0
        self.cantidadparametros = 0
    def primer_trad(self, bandera, code):
        self.bandera = bandera
        self.code = code


        if self.bandera == 6:
            self.codigo.append(str(self.code)+': db 0')

        if self.bandera == 10 or self.bandera == 12:
            if globals()['prim']==0:
                self.codigo.append('section .text \n')
                self.codigo.append('global '+str(self.code)+'\n')
                self.codigo.append('\n'+str(self.code)+':' + '\n \t'  +'PUSH rbp \n\t' + 'MOV rbp, rsp \n\t' 'SUB rsp, 48 \n\t')
                globals()['prim']=1
            else:
                patron = re.compile("[global]+")
                for n in range(len(self.codigo)):
                    if patron.match(self.codigo[n]) != None:

                        self.codigo[n] = self.codigo[n] + ', ' + str(self.code) 
                        break
                        
                    else:
                        pass
                self.codigo.append('\n'+str(self.code)+':' + '\n \t'  +'PUSH rbp \n\t' + 'MOV rbp, rsp \n\t' 'SUB rsp, 48 \n\t')
            globals()['cont']= self.code   

    def segundo_trad(self, bandera, valor, var):
        self.bandera = bandera
        self.valor = valor
        self.var = var
        bandera = 0
        posicionaux =0
        if self.bandera == 21:

            for n in list_ref:
                if self.var == n.var and n.contexto == globals()['cont']:
                    bandera = 1
                    posicionaux = n.pos
                    break
                else:
                    bandera = 0
            if bandera ==1:
                self.codigo.append('\tMOV WORD [rbp -' + str(posicionaux)+'] , '+str(self.valor)+'\n')
            elif bandera == 0:
                self.codigo.append('\tMOV WORD [rbp -' + str(self.posicionvar)+'] , '+str(self.valor)+'\n')
                list_ref.append(refer(self.var, globals()['cont'], self.posicionvar))
                self.posicionvar +=4
                
        if self.bandera == 22:

            for n in list_ref:
                if n.var == self.valor:

                    self.codigo.append('\tMOV rax, QWORD [rbp -' + str(n.pos)+']\n')
                    break
            self.codigo.append('\tMOV QWORD [rbp -' + str(self.posicionvar)+'] , rax \n\t')
            list_ref.append(refer(self.var, globals()['cont'], self.posicionvar))

        if self.bandera == 23:

            self.codigo.append('\tMOV WORD [rbp -' + str(self.posicionvar)+'] , '+str(self.valor))
            list_ref.append(refer(self.var, globals()['cont'], self.posicionvar))
            self.posicionvar +=4

    def op_ret_trad(self, bandera, variables, contexto, num):
        self.bandera = bandera
        self.variables = variables
        self.contexto = contexto
        self.partederecha = num
        i =0
        contador = 0
        vuelta = 0
        bandera = 0
        banderarealizada = 0
        cad = 'MOV rax, '
        cad2 = 'MOV rdi, '
        banderadigito =0
        while contador < self.partederecha:
            for obj in self.variables:
                
                for obj2 in list_ref:
                    if obj.cad == obj2.var and obj.contexto == obj2.contexto and obj.contexto == globals()['cont'] or obj.cad.isdigit() and banderadigito==0:
                        if vuelta == 0:
                            if bandera ==0:
                                if obj.cad.isdigit():
                                    cad = cad + ''+obj.cad
                                    banderadigito=1
                                else:
                                    cad = cad + 'QWORD [rbp -'+ str(obj2.pos)+']'
                                self.codigo.append('\t' + cad +'\n')
                            else:
                                if obj.cad.isdigit():
                                    cad2 = cad2 + ''+obj.cad
                                else:
                                    cad2 = cad2 + 'QWORD [rbp -'+ str(obj2.pos)+']'
                                self.codigo.append('\t' + cad2+'\n')
                            i = 0
                            vuelta += 1
                            contador +=1
                            
                        else:
                            if bandera ==0:
                                if obj.cad.isdigit():
                                    cad2 = cad2 + ''+obj.cad
                                    
                                    
                                else:
                                    cad2 = cad2 + 'QWORD [rbp -'+ str(obj2.pos)+']'
                                self.codigo.append('\t' + cad2+'\n')
                                vuelta += 1
                            else:
                                if self.bandera[0]=='+':
                                    self.codigo.append('\t'+'ADD rax, rdi'+'\n')
                                elif self.bandera[0]=='*':
                                    self.codigo.append('\t'+'MUL rax, rdi'+'\n')
                                elif self.bandera[0]=='-':
                                    self.codigo.append('\t'+'SUB rax, rdi'+'\n')
                                self.bandera.pop(0)
                                banderarealizada= 1
                                vuelta -= 1
                                cad = 'MOV rax, '
                                cad2 = 'MOV rdi, '
                                cad2 = cad2 + 'QWORD [rbp -'+ str(obj2.pos)+']'
                                self.codigo.append('\t' + cad2+'\n')
                                             
                            i = 0
                            
                            contador +=1

                        if (vuelta ==2 or contador >= self.partederecha):
                            try:
                                if self.bandera[0]=='+':
                                    self.codigo.append('\t'+'ADD rax, rdi'+'\n')
                                elif self.bandera[0]=='*':
                                    self.codigo.append('\t'+'MUL rax, rdi'+'\n')
                                elif self.bandera[0]=='-':
                                    self.codigo.append('\t'+'SUB rax, rdi'+'\n')
                                self.bandera.pop(0)
                            except:
                                pass
                            
                            vuelta = 0
                            bandera = 1
                            cad = 'MOV rax, '
                            cad2 = 'MOV rdi, '
                            break
                    else:
                        i+1
                        banderadigito=0

    def op_trad(self, bandera, var1, variables, contexto, num):
        self.bandera = bandera
        self.var1 = var1
        self.variables = variables
        self.contexto = contexto
        self.partederecha = num
        i =0
        contador = 0
        vuelta = 0
        bandera = 0
        banderarealizada = 0
        cad = 'MOV rax, '
        cad2 = 'MOV rdi, '
        banderadigito =0
        while contador < self.partederecha:
            for obj in self.variables:
                
                for obj2 in list_ref:
                    if obj.cad == obj2.var and obj.contexto == obj2.contexto and obj.contexto == globals()['cont'] or obj.cad.isdigit() and banderadigito==0:
                        if vuelta == 0:
                            if bandera ==0:
                                if obj.cad.isdigit():
                                    cad = cad + ''+obj.cad
                                    banderadigito=1
                                else:
                                    cad = cad + 'QWORD [rbp -'+ str(obj2.pos)+']'
                                self.codigo.append('\t' + cad +'\n')
                            else:
                                if obj.cad.isdigit():
                                    cad2 = cad2 + ''+obj.cad
                                else:
                                    cad2 = cad2 + 'QWORD [rbp -'+ str(obj2.pos)+']'
                                self.codigo.append('\t' + cad2+'\n')
                            i = 0
                            vuelta += 1
                            contador +=1
                            
                        else:
                            if bandera ==0:
                                if obj.cad.isdigit():
                                    cad2 = cad2 + ''+obj.cad
                                    
                                    
                                else:
                                    cad2 = cad2 + 'QWORD [rbp -'+ str(obj2.pos)+']'
                                self.codigo.append('\t' + cad2+'\n')
                                vuelta += 1
                            else:
                                if self.bandera[0]=='+':
                                    self.codigo.append('\t'+'ADD rax, rdi'+'\n')
                                elif self.bandera[0]=='*':
                                    self.codigo.append('\t'+'MUL rax, rdi'+'\n')
                                elif self.bandera[0]=='-':
                                    self.codigo.append('\t'+'SUB rax, rdi'+'\n')
                                self.bandera.pop(0)
                                banderarealizada= 1
                                vuelta -= 1
                                cad = 'MOV rax, '
                                cad2 = 'MOV rdi, '
                                cad2 = cad2 + 'QWORD [rbp -'+ str(obj2.pos)+']'
                                self.codigo.append('\t' + cad2+'\n')
                                             
                            i = 0
                            
                            contador +=1

                        if (vuelta ==2 or contador >= self.partederecha):
                            try:
                                if self.bandera[0]=='+':
                                    self.codigo.append('\t'+'ADD rax, rdi'+'\n')
                                elif self.bandera[0]=='*':
                                    self.codigo.append('\t'+'MUL rax, rdi'+'\n')
                                elif self.bandera[0]=='-':
                                    self.codigo.append('\t'+'SUB rax, rdi'+'\n')

                                self.bandera.pop(0)
                                    
                                
                            except:
                                pass
                            
                            vuelta = 0
                            bandera = 1
                            cad = 'MOV rax, '
                            cad2 = 'MOV rdi, '
                            break
                    else:
                        i+1
                        banderadigito=0

        for obj in list_ref:
            if self.var1 == obj.var and self.contexto == obj.contexto:
                self.codigo.append('\t''MOV QWORD [rbp -'+ str(obj.pos)+'], ' + 'rax\n')

    def parametros(self, cantidad, nombre):
        self.cantidad = cantidad
        self.nombre = nombre
        i =0
        if self.comienzo == 0:
            self.comienzo = self.posicionvar +20
        else:
            self.comienzo = self.comienzo
        while i < cantidad:
            self.codigo.append('MOV QWORD [rbp -' +str(self.comienzo)+'], rdi \n')
            list_ref.append(refer(self.nombre, globals()['cont'], self.comienzo))
            i+=1
            self.comienzo+=4


    def func_trad(self):
        if globals()['cont']=='main':
            self.codigo.append('\n\t' 'ADD rsp, 48 \n\t'+ 'MOV rsp, rbp \n\t' +'MOV rax, 60 \n\t'+'MOV rdi, 0 \n\t' + 'syscall \n\t')
        else:
            self.codigo.append('\n\t' 'ADD rsp, 48 \n\t'+ 'MOV rsp, rbp \n\t' +'POP rbp \n\t' + 'ret \n\t')
        self.posicionvar = 4
        self.comienzo = 0

    def trad_ret(self, cad, contexto):
        self.cad = cad
        self.contexto = contexto
        for obj in list_ref:
            if self.cad == obj.var and self.contexto == obj.contexto:
                self.codigo.append('MOV rax, QWORD [rbp -'+ str(obj.pos)+']\n')

    def call_func(self, enviados, llamado, nombre):
        self.enviados = enviados
        self.llamado = llamado
        self.nombre = nombre
        for obj in list_ref:
            if self.enviados == obj.var and globals()['cont'] == obj.contexto:
                self.codigo.append('\t''MOV rax, QWORD [rbp -'+ str(obj.pos)+']\n')
        self.codigo.append('\t''MOV rdi, rax')
        self.codigo.append('\n\t''call '+ str(nombre))
        for obj in list_ref:
            if self.llamado == obj.var and globals()['cont'] == obj.contexto:
                self.codigo.append('\n\t''MOV QWORD [rbp -'+ str(obj.pos)+'], rax\n\t')
    
    def call_funcnum(self, enviados, llamado, nombre):
        self.enviados = enviados
        self.llamado = llamado
        self.nombre = nombre
        vuelta = 0
        for obj in self.enviados:
            self.codigo.append('\t''MOV ax,' +str(obj.cad)+ '\n')
            if vuelta == 0:
                
                self.codigo.append('\t''MOV rdi, rax')
                vuelta+=1
            elif vuelta ==1:
                self.codigo.append('\t''MOV rsi, rax')
        
        self.codigo.append('\n\t''call '+ str(nombre))
        for obj in list_ref:
            if self.llamado == obj.var and globals()['cont'] == obj.contexto:
                self.codigo.append('\n\t''MOV QWORD [rbp -'+ str(obj.pos)+'], rax\n\t')
     
    def print_func(self, valor):
        for obj in list_ref:
            if obj.var == valor and globals()['cont'] == obj.contexto:
                self.codigo.insert(0, 'section .data  \n\tprimr: db  "La impresion es := %lf",10,0 \nsection .bss \n\tresp: resq 2\n')
                self.codigo.insert(2, '\nextern printf\n')
                self.codigo.append('\n\tPUSH qword[rbp -'+str(obj.pos)+']')
                self.codigo.append('\n\tFILD dword[rsp]')
                self.codigo.append('\n\tFSTP qword[rel resp]')
                self.codigo.append('\n\tADD rsp, 8')
                self.codigo.append('\n\tMOVSD xmm0,qword[rel resp]')
                self.codigo.append('\n\tMOV rdi, primr')
                self.codigo.append('\n\tMOV al, 1')
                self.codigo.append('\n\tcall printf WRT ..plt \n\t')

    def gettraduccion(self):
        for obj in self.codigo:
            print(obj)
        Archivo=open("Proyecto final/Ensamblador.asm","w")
        for i in range(len(self.codigo)):
            Archivo.write(self.codigo[i])   
        del self.codigo[:]
        Archivo.close()



    def __repr__(self):
        aux = ("Variable: "+str(self.var)+ " Contexto: "+str(self.contexto)+ " Pos: "+str(self.pos))
        return aux





code = traduccion_sasm()
list_lex = list()
list_er_lex = list()
list_er = list()
lista_pila = list()
list_reglas = list()
auxil_reglas = list()
matr_regl = list()
lista_variables = list()
lista_var = list()
lista_funciones = list()
list_definiciones = list()
list_def = list()
list_def_arbol = list()
list_param = list()
list_term = list()
list_term_aux = list()
list_expres = list()
list_sent = list()
list_local = list()
list_param_id = list()
llist_llama = list()
llist_ret = list()
list_op = list()
list_sent_bloque = list()

globals()['ban_var_1']=0
globals()['ban_var_2']=0
globals()['ban_term'] = 0
globals()['cont']=''
globals()['call']=0
globals()['igual']=0
globals()['rel']=0
globals()['multi']=0
globals()['ban_lex']=0
globals()['tipo_ret'] =""
globals()['v_print']=''
globals()['ban_print']= 0
globals()['call_func'] = 0
globals()['rev_error'] = 0

def rev_regl():
    file = open('Proyecto Final/compilador.lr', 'r')
    line = file.readlines()
    for m in line:
        m = m.rstrip()
        matr_regl.append(m.split('\t'))

    for m in range (len(matr_regl)):
        for n in range(len(matr_regl[m])):
            matr_regl[m][n] = int(matr_regl[m][n])
    file.close()

def auxil_regl():
    n = 1
    file = open('Proyecto final/rgl.txt', 'r')
    line = file.readlines()
    for m in line:
        m = m.rstrip()
        auxil_reglas.append(m.split('\t'))

    for m in auxil_reglas:
        m = Regla(n, int(m[0]), int(m[1]), str(m[2]))
        n+=1
        list_reglas.append(m)
    file.close()

def buscar_lex(str):
        for n in list_lex:
            if n.cad == str:
                return n
            else:
                pass

raiz = Node(10)
globals()['bandera']=0

class Definicion_Var(Nodo):
    def __init__(self, data, tipo, lv):
        Nodo.__init__(self, data)
        self.tipo = tipo
        self.lv = lv

    def eliminaVar(self):
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        self.lv = lista_pila.pop()
        lista_pila.pop()
        self.data = lista_pila.pop()
        lista_pila.pop()
        self.tipo = lista_pila.pop()
        self.lv = globals()['cont']
        if self.lv == '':
            self.lv = 'Global'
        lista_variables.append(Definicion_Var(self.tipo, self.data, self.lv))
        globals()['actual']= Node(Definicion_Var(self.tipo, self.data, self.lv), parent = raiz)
        globals()['ban_var_2'] +=1
        
        if len(lista_var)!=0:
            for i in range(len(lista_var)):
                auxiliar = lista_var.pop(0)
                auxiliar.data = self.tipo
                auxiliar.lv = self.lv
                lista_var.append(auxiliar)
                lista_variables.append(auxiliar)
            
            
    def eliminalistaVar(self):
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        self.data = lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        lista_var.append(Definicion_Var('Unknown ', self.data, self.lv))
        
    def __repr__(self):
        objeto = ("Variable""\n \t \t \t" "Tipo: "+str(self.data.cad)+ " ID: "+str(self.tipo.cad)+ " Contexto: "+str(self.lv))
        return objeto

class Definicion_Funcion(Nodo):
    def __init__(self, data, id, tipo):
        Nodo.__init__(self, data)
        self.id = id
        self.tipo = tipo

    def eliminaFunc(self):
        aux = globals()['cont']
        globals()['cont'] =''
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        id =lista_pila.pop()
        lista_pila.pop()
        tipo= lista_pila.pop()
        if globals()['tipo_ret'] != tipo.cad:
            if globals()['tipo_ret'] == '':
                pass
            else:
                list_er.append('Error de retorno ' + aux + ' sin tipos de datos diferentes')
        globals()['tipo_ret'] = ""
        lista_funciones.append(Definicion_Funcion(self.data, id, tipo))
        if len(list_param)!=0:
             globals()['auxiliarFunc'] = Node(Definicion_Funcion(self.data, id, tipo), parent = raiz)
             for i in range (len(list_param)):
                auxiliar = list_param.pop()
                auxiliar.parent = globals()['auxiliarFunc']
             globals()['auxiliarBlo'].parent =auxiliar
        else:
            globals()['auxiliarFunc'] = Node(Definicion_Funcion(self.data, id, tipo), parent = raiz)
            globals()['auxiliarBlo'].parent = globals()['auxiliarFunc'] 
        code.func_trad()
        list_op.clear()
    def __repr__(self):
        objeto = ("Definicion_Funcion""\n" "Tipo: "+str(self.tipo.cad)+ " ID: "+str(self.id.cad))
        return objeto

class Bloque_Funcion(Nodo):
    def __init__(self, data, bandera):
        Nodo.__init__(self, data)
        self.bandera = bandera
    def eliminaBlo(self):
        list_term.clear()
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        self.bandera = 0
        globals()['auxiliarBlo'] = Node(Bloque_Funcion(self.data, self.bandera), parent = raiz)
        globals()['auxiliarLocales'].parent = globals()['auxiliarBlo'] 
        
    def eliminaBloque(self):
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        self.bandera = 1
        globals()['auxiliarBlo'] = Node(Bloque_Funcion(self.data, self.bandera), parent = raiz)
        try:
            globals()['sentencias'].parent = globals()['auxiliarBlo'] 
        except:
            globals()['expresionRel'].parent = globals()['auxiliarBlo'] 
    def __repr__(self):
        if self.bandera == 1:
            objeto = ('Bloque')
        else:
            objeto = ('BloqueFunc')
        return objeto

class Parametros(Nodo):
    def __init__(self, data, id, tipo):
        Nodo.__init__(self, data)
        self.id = id
        self.tipo = tipo
    def eliminaPara(self):
        
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        self.id = lista_pila.pop()
        lista_pila.pop()
        self.tipo= lista_pila.pop()
        globals()['parametro'] = Node(Parametros(self.data, self.id, self.tipo), parent = raiz)
        list_param.append(globals()['parametro'])
        contexto = ""
        i = 0
        posi =2
        posfi = 6
        if lista_pila[2]=='Definicion':
            while i == 0: 
                posi = posi +2
                if lista_pila[posi] == 'Definicion':
                    posfi = posfi +2
                else:
                    contexto =lista_pila[posfi].cad
                    i = 1
                    break
        else:
            contexto= lista_pila[4].cad
        list_param_id.append(Seg_Parametros(self.tipo.cad, self.id.cad, contexto ))
        
        code.parametros(1, self.id.cad)
        
    def eliminalistaPara(self):
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        self.id = lista_pila.pop()
        lista_pila.pop()
        self.tipo= lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        globals()['parametro'] = Node(Parametros(self.data, self.id, self.tipo), parent = raiz)
        list_param.append(globals()['parametro'])
        i = 0
        posi =2
        posfi = 6
        contexto = ''
        if lista_pila[2]=='Definicion':
            while i == 0: 
                posi = posi +2
                if lista_pila[posi] == 'Definicion':
                    posfi = posfi +2
                else:
                    contexto =lista_pila[posfi].cad
                    i = 1
                    break
        else:
            contexto= lista_pila[4].cad
        list_param_id.append(Seg_Parametros(self.tipo.cad, self.id.cad, contexto))
        code.parametros(1, self.id.cad)
    def __repr__(self):
        objeto = ('Parametros' '\n'+ ' Tipo: '+str(self.tipo.cad)+' Id: '+str(self.id.cad))
        return objeto

class Definicion_Local(Nodo):
    def __init__(self, data):
        Nodo.__init__(self, data)
        self.banderalocal=0

    def eliminaVar(self):
        lista_pila.pop()
        lista_pila.pop()
        if self.banderalocal==0:
            globals()['auxiliarLocal'] = Node(Definicion_Local(self.data), parent = raiz)
            
            globals()['actual'].parent = globals()['auxiliarLocal']
            if len(lista_var)!=0:
                for i in range(len(lista_var)):
                    auxiliar = lista_var.pop(0)
                    globals()['actual']= Node(auxiliar, parent = globals()['auxiliarLocal'])
            
            self.banderalocal=1
        else:
            globals()['actual'].parent = globals()['auxiliarLocal']
            
    def flagreset(self):
        self.banderalocal=0

    def eliminaSen(self):
        lista_pila.pop()
        lista_pila.pop()
        
        globals()['auxiliarLocalSen'] = Node(Definicion_Local(self.data), parent = raiz)
        globals()['sentencia'].parent = globals()['auxiliarLocalSen']
        list_local.append(globals()['auxiliarLocalSen'])

        if globals()['ban_print'] == 1:
            code.print_func(globals()['v_print'])
            globals()['ban_print'] = 0

    def __repr__(self):
        objeto = ('Definicion_Local')
        return objeto

class Definicion_Locales(Nodo):
    def __init__(self, data):
        Nodo.__init__(self, data)
        self.banderalocal=0
    def eliminaDef(self):
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        if self.banderalocal == 0: 
            globals()['auxiliarLocales'] = Node(Definicion_Locales(self.data), parent = raiz)
            if len(list_local)!=0:
                aux = list_local.pop()
                aux.parent = globals()['auxiliarLocales'] 
            else:
                globals()['auxiliarLocal'].parent = globals()['auxiliarLocales'] 
            self.banderalocal=1
        else:
            if len(list_local)!=0:
                aux = list_local.pop()
                aux.parent = globals()['auxiliarLocales'] 
            else:
                globals()['auxiliarLocal'].parent = globals()['auxiliarLocales'] 
             
    def __repr__(self):
        objeto = ('Definicion_Locales')
        return objeto

class Definiciones(Nodo):
    def __init__(self, data, ultimadef):
        Nodo.__init__(self, data)
        self.ultimadef = ultimadef
    def eliminaDefiniciones(self):
        
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        definicion = self.ultimadef
        list_definiciones.append(definicion)
        globals()['auxiliarDefiniciones'] = Node(Definiciones(self.data, definicion), parent = raiz)
        auxiliar= list_def_arbol.pop()
        auxiliar.parent = globals()['auxiliarDefiniciones'] 
    def __repr__(self):
        objeto = ("Definiciones")
        return objeto

class Argumentos(Nodo):
    def __init__(self, data):
        Nodo.__init__(self, data)
    def eliminaarg(self):
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        globals()['argumentos'] = Node(Argumentos(self.data), parent = raiz)
        globals()['expresion'].parent = globals()['argumentos'] 
    def eliminalistaarg(self):
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
    def __repr__(self):
        objeto = ('Argumentos')
        return objeto

class Llamada_Funcion(Nodo):
    def __init__(self, data, funcion):
        Nodo.__init__(self, data)
        self.funcion = funcion
        self.listanum = list()
    def eliminallamada(self):
        globals()['call_func']=1
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        self.data = lista_pila.pop()
        bandera = 0
        bandera2 =0
        print(list_param_id)
        bandera3 = 0
        contexto  = ''
        i = 0
        posi =2
        posfi = 6
        if lista_pila[2]=='Definicion':
            while i == 0: 
                posi = posi +2
                if lista_pila[posi] == 'Definicion':
                    posfi = posfi +2
                else:
                    contexto =lista_pila[posfi].cad
                    i = 1
                    break
        else:
            contexto= lista_pila[4].cad
            
        if len(list_param_id)!=0:
            for obj in list_param_id:
                if self.data.cad == obj.tipo:
                    self.funcion= obj.tipo
                    
                    try:
                        print(list_term[-1].cad)
                    except:
                        bandera=1
                        break
                    for obj2 in lista_variables:

                        if list_term[-1].cad == obj2.tipo.cad and obj2.lv == contexto:
                            if obj.data == obj2.data.cad:
                                bandera = 0
                                bandera2=0
                                code.call_func(obj2.tipo.cad, lista_pila[-4].cad, self.data.cad)
                                if bandera3 ==0:
                                    globals()['llam_fun'] = Node(Llamada_Funcion(self.data, self.funcion), parent = raiz)
                                    globals()['argumentos'].parent = globals()['llam_fun']
                                    bandera3+=1
                                else:
                                    pass
                                num = list_param_id.index(obj)
                                self.listanum.append(num)
                                list_term.pop()
                                break
                            else:
                                bandera = 1
                        else:
                            bandera2=1
                    
                    if bandera2 ==1:
                        tipo = ''
                        if list_term[-1].tipo == 'Entero':
                            tipo = 'int'
                        elif list_term[-1].tipo == 'Real':
                            tipo = 'float'
                        if tipo == obj.data:
                            globals()['llam_fun'] = Node(Llamada_Funcion(self.data, self.funcion), parent = raiz)
                            globals()['argumentos'].parent = globals()['llam_fun'] 
                            break
                        else:
                            bandera = 1
                            

                    else:
                        pass
                else:
                    pass
            tipo = ''
            tipo2 = ''
            if len(llist_ret)>0:
                for obj in llist_ret:
                    if self.funcion== obj.context:
                        tipo = obj.tipo
            else:
                tipo = 'void'

            for obj in lista_variables:
                if obj.tipo.cad == lista_pila[-4].cad and obj.lv == contexto:
                    tipo2 = obj.data.cad
            if tipo != tipo2:
                if tipo == 'void':
                    pass
                else:
                    list_er.append('Error de retorno ' + self.data.cad + ' sin tipos de datos diferentes')
            if bandera == 1:
                list_er.append('Error de llamada a funcion ' + self.data.cad + ' sin tipos de datos diferentes')
                globals()['llam_fun'] = Node(Llamada_Funcion(self.data, self.funcion), parent = raiz)
                globals()['argumentos'].parent = globals()['llam_fun'] 
            globals()['call']=1
        
    def __repr__(self):
        objeto = ('LlamadaFunc' + ' ID: ' + str(self.funcion))
        return objeto

class Definicion(Nodo):
    def __init__(self, data, ultima):
        Nodo.__init__(self, data)
        self.ultima = ultima
    def eliminaDefVar(self):
        lista_pila.pop()
        lista_pila.pop()
        for obj in lista_variables:
            if obj == self.ultima:
                globals()['auxiliarVar']= Node(Definicion(self.data, obj), parent = raiz)
                globals()['actual'].parent = globals()['auxiliarVar']
                list_def_arbol.append(globals()['auxiliarVar'])
                list_def.append(obj)

    def eliminaDef(self):
        lista_pila.pop()
        lista_pila.pop()
        for obj in lista_funciones:
            if obj == self.ultima:
                globals()['auxiliarDefinicion'] = Node(Definicion(self.data, obj), parent = raiz)
                globals()['auxiliarFunc'].parent = globals()['auxiliarDefinicion']
                list_def_arbol.append(globals()['auxiliarDefinicion'])
                list_def.append(obj)
                
                self.contadordefinicion+=1

    def __repr__(self):
        objeto = ("Definicion")
        return objeto



class Programa(Nodo):
    def __init__(self, data):
        Nodo.__init__(self, data)

    def programaexitoso(self):
        lista_pila.pop()
        lista_pila.pop()
        raiz.name = "Programa"
        

class Termino(Nodo):            
    def __init__(self, data, tipo, lv):
        Nodo.__init__(self, data)
        self.tipo = tipo
        self.lv = lv
    def eliminaTerminoEntero(self):
        lista_pila.pop()
        self.data = lista_pila.pop()
        self.lv = globals()['cont']
        try:
            if lista_pila[14].cad=='return':
                i = 0
                contexto = ''
                posi =2
                posfi = 6
                if lista_pila[2]=='Definicion':
                    while i == 0: 
                        posi = posi +2
                        if lista_pila[posi] == 'Definicion':
                            posfi = posfi +2
                        else:
                            contexto =lista_pila[posfi].cad
                            i = 1
                            break
                    globals()['termino'] = Node(Termino(self.data, self.tipo, 'Retorno '+contexto), parent = raiz)
                else:
                    globals()['termino'] = Node(Termino(self.data, self.tipo, 'Retorno '+lista_pila[4].cad), parent = raiz)
            else:
                globals()['termino'] = Node(Termino(self.data, self.tipo, self.lv), parent = raiz)
        except:
            globals()['termino'] = Node(Termino(self.data, self.tipo, self.lv), parent = raiz)
        list_term.append(self.data)

    def eliminaTerminoFloat(self):
        lista_pila.pop()
        self.data = lista_pila.pop()
        try:
            if lista_pila[14].cad=='return':
                i = 0
                contexto = ''
                posi =2
                posfi = 6
                if lista_pila[2]=='Definicion':
                    while i == 0: 
                        posi = posi +2
                        if lista_pila[posi] == 'Definicion':
                            posfi = posfi +2
                        else:
                            contexto =lista_pila[posfi].cad
                            i = 1
                            break
                    globals()['termino'] = Node(Termino(self.data, self.tipo, 'Retorno '+contexto), parent = raiz)
                else:
                    globals()['termino'] = Node(Termino(self.data, self.tipo, 'Retorno '+lista_pila[4].cad), parent = raiz)
            else:
                globals()['termino'] = Node(Termino(self.data, self.tipo, self.lv), parent = raiz)
        except:
            globals()['termino'] = Node(Termino(self.data, self.tipo, self.lv), parent = raiz)
        list_term.append(self.data)

    def eliminaTerminoId(self):
        lista_pila.pop()
        self.data = lista_pila.pop()
        
        i =globals()['ban_var_1']
        largo = len(lista_variables)
        correcto = 0
        while i <globals()['ban_var_2']:
            if self.data.cad == lista_variables[i].tipo.cad:
                self.tipo = lista_variables[i].data
                self.lv = lista_variables[i].lv
                correcto = 1
                break
            i+=1
            largo-=1
            correcto = 0
        flagencontrado = 0
        if largo <=0 and correcto == 0:
            for obj in list_param_id:
                if obj.id == self.data.cad:
                    flagencontrado = 0
                    break
                else: 
                    flagencontrado = 1
        if flagencontrado==1:
            list_er.append('Error de variable ' + str(self.data.cad) +' inexistente')
        try:
            if lista_pila[-2].cad=='return' or lista_pila[16].cad == 'return':
                contexto =""
                i = 0
                posi =2
                posfi = 6
                if lista_pila[2]=='Definicion':
                    while i == 0: 
                        posi = posi +2
                        if lista_pila[posi] == 'Definicion':
                            posfi = posfi +2
                        else:
                            contexto =lista_pila[posfi].cad
                            i = 1
                            break
                else:
                    contexto= lista_pila[4].cad
                globals()['termino'] = Node(Termino(self.data, self.tipo, 'Retorno '+contexto), parent = raiz)
            else:
                globals()['termino'] = Node(Termino(self.data, self.tipo, self.lv), parent = raiz)
        except:
            globals()['termino'] = Node(Termino(self.data, self.tipo, self.lv), parent = raiz)
        list_term.append(self.data)

    def eliminaTerminoLlamada(self):
        lista_pila.pop()
        lista_pila.pop()
        globals()['termino'] = Node(Termino('LLamada', 'Llamada', 'Llamada'), parent = raiz)
        try:
            
            globals()['llam_fun'].parent = globals()['termino'] 
        except:
            globals()['llam_fun'] = Node(Termino('LLamada', 'Llamada', 'Llamada'), parent = raiz)
            globals()['llam_fun'].parent = globals()['termino'] 
            list_er.append('Error en la llamada')
        auxiliar = list_def_expr[-1]
        auxiliar.flagreset()
        llist_llama.append('Llamada')
    def __repr__(self):
        try:
            objeto = ('Termino' + ' Id: '+str(self.data.cad) + ' Contexto: '+str(self.lv))
        except:
            objeto = ('Termino')
            globals()['ban_term'] = 0
        return objeto

class Sentencia(Nodo):
    def __init__(self, data, aux):
        Nodo.__init__(self, data)
        self.listateraux = list()
        self.aux = aux
    def eliminaSen(self):
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        self.data = lista_pila.pop()
        globals()['sentencia'] = Node(Sentencia(self.data, self.aux), parent = raiz)
        list_sent.append(globals()['sentencia'])
        cont =0
        try:
            if list_expres[-1]==globals()['expresionSum']:
                globals()['expresionSum'].parent = globals()['sentencia']
            else:
                pass
        except:
            pass
        try:
            if list_expres[-1]==globals()['']:
                globals()['expresionRel'].parent = globals()['sentencia']
            else:
                pass
        except:
            pass
        if len(llist_llama)!=0 or len(list_expres)!=0:
            if globals()['rel'] ==1:
                globals()['expresionRel'].parent = globals()['sentencia']
                globals()['rel'] =0
            elif globals()['multi'] ==1:
                globals()['expresionMul'].parent = globals()['sentencia']
                globals()['multi']=0
            elif globals()['igual'] ==1:
                globals()['expresionIgu'].parent = globals()['sentencia']
                globals()['igual']=0
            else:
                globals()['expresion'].parent = globals()['sentencia']
            llist_llama.clear()
        list_expres.clear()
        anadidos = 0
        x = 0
        partederecha = 0
        if list_expres!=0:
            
            for obj in lista_variables:
                if self.data.cad == obj.tipo.cad and obj.lv == globals()['cont']:
                    aux= obj.data.cad
                    aux2 = obj
                    cont = 0
                    while x < anadidos:
                        list_er.pop()
                        x+=1
                    break
                else:
                    if cont ==0:
                        cont = 1
                        list_er.append('Error de asignacion ' + str(self.data.cad) +' variable inexistente o fuera de contexto')
                        aux = 'mmm'
                        aux2 = 'mmm'
                        anadidos +=1
                    else:
                        pass

            for obj in list_term:
                self.listateraux.append(obj)
            i =0
            coincidencias = len(self.listateraux)
            coincidenciasobj = 0
            variables = list()
            bandera = 0
            correcto = 0
            largo = len(lista_variables)
            for obj in lista_variables:
                if bandera == 1:
                    break
                if coincidenciasobj == coincidencias:
                    break
                for obj2 in self.listateraux:
                    if obj.tipo.cad == self.listateraux[i].cad:
                        bandera = 0
                        correcto = 1
                        coincidenciasobj +=1
                        if obj.data.cad != aux:
                            if cont ==0:
                                list_er.append('Error asignacion ' + str(aux2.tipo.cad) +' datos diferentes')
                                bandera = 1
                                cont+=1
                        else:
                            pass
                    else:
                        largo -=1
                        correcto =0
                        pass                        

                    i +=1
                i=0
            if largo <=0 and correcto == 0 and coincidenciasobj != coincidencias:
                if len(lista_variables)==0:
                    list_er.append('Error asignacion ' + str(self.data.cad) +' Contexto inexistente')
                    cont+=1
                else:
                    bandera =1
            contador = 0
            esparametro= 0
            if bandera ==1:
                if obj2.tipo == 'Real':
                    obj2.tipo = 'float'
                elif obj2.tipo == 'Entero':
                    obj2.tipo = 'int'
                elif obj2.tipo == 'Identificador':
                    esparametro= 1
                    for objeto in list_param_id:
                        if objeto.id == self.listateraux[contador].cad:
                            obj2.tipo = objeto.data
                            break
                        else: 
                            pass
                            
                if obj2.tipo != aux:
                    if globals()['call']!=0:
                        pass
                    else:
                        if cont ==0:
                            list_er.append('Error de asignacion ' + str(aux2.tipo.cad) +' datos diferentes')
                            cont+=1
                else:
                    if len(list_op):
                        if globals()['call_func'] == 0:
                            if esparametro== 0:
                        
                                code.segundo_trad(21, obj2.cad, aux2.tipo.cad)
                            else:
                                code.segundo_trad(22, obj2.cad, aux2.tipo.cad)
                    else:
                        pass
            if cont ==0 and len(list_op)!=0:
                for obj5 in list_term:
                    variables.append(Variables(obj5.cad, globals()['cont']))
                partederecha = len(variables)
                if list_op[0] == '+' or list_op[0] == '*':
                    code.op_trad(list_op, obj.tipo.cad, variables, globals()['cont'], partederecha)
                    pass
            for m in list_term_aux:
                list_term_aux.append(m)
            list_term.clear()
            list_op.clear()
            globals()['call']=0

            if globals()['ban_print'] == 1:
                code.print_func(globals()['print'])
            globals()['ban_print'] = 0
            globals()['v_print']=''
            
        else:
            pass
        self.aux = 'Sentencia'
    def eliminavalor(self):
            lista_pila.pop()
            lista_pila.pop()
            lista_pila.pop()
            lista_pila.pop()
            self.data = list_term.pop()
            globals()['sentencia'] = Node(Sentencia(self.data, self.aux), parent = raiz)
            list_sent.append(globals()['sentencia'])
            globals()['expresion'].parent = globals()['sentencia']
            lista_pila.pop()
            lista_pila.pop()
            self.aux = 'Sentencia'
    def eliminaSentencias(self):
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        self.data = lista_pila.pop()
        globals()['sentencias'] = Node(Sentencia(self.data, self.aux), parent = raiz)
        list_sent.append(globals()['sentencias'])
        try:
            if list_expres[-1]==globals()['expresionSum']:
                globals()['expresionSum'].parent = globals()['sentencias']
            else:
                pass
        except:
            pass
        try:
            if list_expres[-1]==globals()['expresionRel']:
                globals()['expresionRel'].parent = globals()['sentencias']
            else:
                pass
        except:
            pass
        
        globals()['sentencia'].parent = globals()['sentencias']
        llist_llama.clear()
        
        self.aux = 'Sentencias'
    def eliminaSentenciaBloque(self):
        lista_pila.pop()
        lista_pila.pop()
        globals()['SentenciaBloque'] = Node(Sentencia(self.data, self.aux), parent = raiz)
        globals()['auxiliarBlo'].parent = globals()['SentenciaBloque']
        self.aux = 'Sentencia Bloque'

    def __repr__(self):
        return self.aux

class Expresion(Nodo):
    def __init__(self, data):
        Nodo.__init__(self, data)
        self.banderalocal=0
    def eliminaTer(self):
        lista_pila.pop()
        self.data = lista_pila.pop()
        if self.banderalocal == 0: 
            globals()['expresion'] = Node(Expresion(self.data), parent = raiz)
            list_expres.append(globals()['expresion'])
            globals()['termino'].parent = globals()['expresion']
            self.banderalocal=1
        else:
            globals()['termino'].parent = globals()['expresion']
        list_expres.append(globals()['expresion'])
    def eliminaMul(self):
        list_term_aux.clear()
        list_op.append('*')
        lista_pila.pop()
        self.data = lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        globals()['expresionMul'] = Node(Expresion(self.data), parent = raiz)
        globals()['expresion'].parent = globals()['expresionMul']
        list_expres.append(globals()['expresionMul'])
        globals()['multi']=1

    def eliminaSum(self):
        list_term_aux.clear()
        list_op.append(str(lista_pila[-4].cad))
        lista_pila.pop()
        self.data = lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        globals()['expresionSum'] = Node(Expresion(self.data), parent = raiz)
        globals()['expresion'].parent = globals()['expresionSum']
        list_expres.append(globals()['expresionSum'])

    def eliminarelacional(self):
        lista_pila.pop()
        self.data = lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        globals()['expresionRel'] = Node(Expresion(self.data), parent = raiz)
        globals()['expresion'].parent = globals()['expresionRel']
        list_expres.append(globals()['expresionRel'])
        globals()['rel']=1
        list_term_aux.clear()
    
    def eliminaigualdad(self):
        lista_pila.pop()
        self.data = lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        lista_pila.pop()
        globals()['expresionIgu'] = Node(Expresion(self.data), parent = raiz)
        globals()['expresion'].parent = globals()['expresionIgu']
        list_expres.append(globals()['expresionIgu'])
        globals()['igualdad']=1
        list_term_aux.clear()

    def flagreset(self):
        self.banderalocal=0
    def __repr__(self):
        objeto = ('Expresion')
        return objeto

list_def_loc= list()
list_def_locales= list()
list_def_expr= list()
globals()['ban_c']=0
globals()['ban_p']=0

###########Analizador Lexico###########
class analizador:
    def __init__(self, cadena_para_analizar):
        self.cadena_analizada = cadena_para_analizar +"~"
        self.edo = 0
        self.i = 0
        self.tmp =""
        self.continua = True
        self.tipo=list()
        self.aux = 0
        

    def anlexico(self):
        
        while self.continua:
            c = self.cadena_analizada[self.i]
            
            if self.edo == 0:                                            
                if c >= "0" and c <= "9":
                    self.edo = 1
                    self.tmp +=c
                    
                elif c == "E":
                    self.tmp +=c
                    self.tipo.append(3)
                    objlex = No_Terminal("E","E",self.tipo[-1])
                    list_lex.append(objlex)
                    self.continua = False
                    
                elif c >= "a" and c <= "z" or c >= "A" and c <= "Z" or c == "_":
                    self.edo = 4
                    self.tmp += c
                elif c == " ":
                    self.edo = 0

                elif c == "'" or c=='"':
                    self.edo = 9
                    self.tmp +=c

                elif (c == "*") or (c == "/"):
                    self.edo = 0
                    self.tmp +=c
                    self.tipo.append(6)
                    objlex = Terminal(self.tmp, 'Op. Mul', self.tipo[-1])
                    list_lex.append(objlex)
                    self.limpieza()

                elif (c == "=") or (c == "!"):
                    self.limpieza()
                    self.edo = 5
                    self.tmp +=c
                
                elif (c == "<") or (c == ">"):    
                    self.limpieza()
                    self.edo = 6
                    self.tmp +=c
                elif (c == "|"):   
                    self.limpieza()
                    self.edo = 7
                    self.tmp +=c
                elif (c == "&"):    
                    self.limpieza()
                    self.edo = 8
                    self.tmp +=c

                
                elif (c == "+") or (c == "-"):
                    if self.aux == 1:
                        self.tipo.append(5)
                        objlex = Terminal(self.tmp, 'Op. Suma', self.tipo[-1])
                        list_lex.append(objlex)
                        self.limpieza()

                    elif self.aux == 2:
                        
                        self.limpieza()
                    if c =="+":
                        self.tmp +=c
                        self.tipo.append(5)
                        objlex = Terminal(self.tmp, 'Op. Suma', self.tipo[-1])
                        list_lex.append(objlex)
                        self.limpieza()
                        self.edo = 0
                    else:
                        self.tmp +=c
                        self.tipo.append(5)
                        objlex = Terminal(self.tmp, 'Op. Suma', self.tipo[-1])
                        list_lex.append(objlex)
                        self.limpieza()
                        self.edo = 0

                elif c == ";":
                    self.tmp +=c
                    self.tipo.append(12)
                    objlex = Terminal(self.tmp, 'Punto y coma', self.tipo[-1])
                    list_lex.append(objlex)
                    self.limpieza()
                    self.edo = 0
                    
                
                elif c == ",":
                    self.tmp +=c
                    self.tipo.append(13)
                    objlex = Terminal(self.tmp, 'Coma', self.tipo[-1])
                    list_lex.append(objlex)
                    self.limpieza()
                    self.edo = 0
                    
                    
                
                elif c == "$":
                    self.tmp +=c
                    self.tipo.append(23)
                    objlex = Terminal(self.tmp, 'Op. $', self.tipo[-1])
                    list_lex.append(objlex)
                    self.edo = 0
                elif c == "(":
                    self.tmp +=c
                    self.tipo.append(14)
                    objlex = Terminal(self.tmp, 'Parentesis Iz', self.tipo[-1])
                    list_lex.append(objlex)
                    self.edo = 0
                    globals()['ban_p']+=1
                    self.limpieza()
                elif c == ")":
                    self.tmp +=c
                    self.tipo.append(15)
                    objlex = Terminal(self.tmp, 'Parentesis Der', self.tipo[-1])
                    list_lex.append(objlex)
                    self.limpieza()
                    if globals()['ban_p']!=0:
                        globals()['ban_p']-=1
                    else:
                        list_er_lex.append('Error, parentesis sin cerrar ')

                    self.edo = 0

                elif c == "{":
                    self.tmp +=c
                    self.tipo.append(16)
                    objlex = Terminal(self.tmp, 'Corchete Iz', self.tipo[-1])
                    list_lex.append(objlex)
                    self.edo = 0
                    globals()['ban_c']+=1
                    self.limpieza()
                elif c == "}":
                    self.tmp +=c
                    self.tipo.append(17)
                    objlex = Terminal(self.tmp, 'Corchete Der', self.tipo[-1])
                    list_lex.append(objlex)
                    self.limpieza()
                    if globals()['ban_c']!=0:
                        globals()['ban_c']-=1
                    else:
                        list_er_lex.append('Error, corchetes sin cerrar ')
                    self.edo = 0
                
                elif c == "~":
                    self.continua=False
                
            elif self.edo == 1:                                   
                if c >= "0" and c <= "9":
                    self.edo = 1
                    self.tmp +=c

                elif c == ".":
                    self.edo = 2
                    self.tmp += c

                elif c == " ":
                    self.edo = 0
                    self.tipo.append(1)
                    objlex = Terminal(self.tmp, 'Entero', self.tipo[-1])
                    list_lex.append(objlex)
                    self.limpieza()

                elif c == "~":
                    self.tipo.append(1)
                    objlex = Terminal(self.tmp, 'Entero', self.tipo[-1])
                    list_lex.append(objlex)
                    self.continua = False
                else:
                    self.tipo.append(1)
                    objlex = Terminal(self.tmp, 'Entero', self.tipo[-1])
                    list_lex.append(objlex)
                    self.limpieza()
                    self.edo = 0
                    self.aux = 1
                    self.i-=1

            elif self.edo == 2:                                
                if c >= "0" and c <= "9":
                    self.edo = 3
                    self.tmp +=c
            
            elif self.edo == 3:                               
                if c >= "0" and c <= "9":
                    self.edo = 3
                    self.tmp +=c
                    
                
                elif c == " ":
                    self.edo = 0

                elif c == "~":
                    self.tipo.append(2)
                    objlex = Terminal(self.tmp, 'Real', self.tipo[-1])
                    list_lex.append(objlex)
                    self.limpieza()
                    self.continua = False
                else:
                    self.tipo.append(1)
                    objlex = Terminal(self.tmp, 'Real', self.tipo[-1])
                    list_lex.append(objlex)
                    self.limpieza()
                    self.edo = 0
                    self.i-=1

            elif self.edo == 4:                                                                        
                if c >= "a" and c <= "z" or c >= "A" and c <= "Z" or c == "_" or c >= "0" and c <= "9":
                    self.edo = 4
                    self.tmp +=c
                elif c == " ":
                    self.reservado()
                    self.limpieza()
                    self.edo = 0

                elif c == "~":
                    self.reservado()
                    self.continua = False
                else:
                    self.reservado()
                    self.edo = 0
                    self.limpieza()
                    self.i-=1
                    self.aux=2
            
            elif self.edo == 5:                                
                if c == "=":
                    self.edo = 0
                    self.tmp +=c
                    self.tipo.append(11)
                    objlex = Terminal(self.tmp, 'Op. Igualdad', self.tipo[-1])
                    list_lex.append(objlex)
                    self.limpieza()
                
                elif c == " ":
                    self.edo = 0

                elif c == "~":
                    if self.cadena_analizada[self.i-1]=="=":
                        self.edo = 0
                        self.tipo.append(18)
                        objlex = Terminal(self.tmp, 'Op. Igual', self.tipo[-1])
                        list_lex.append(objlex)
                        self.limpieza()
                    else:
                        self.limpieza()
                    self.continua = False
                else:
                    if self.cadena_analizada[self.i-1]=="=":
                        self.edo = 0
                        self.tipo.append(18)
                        objlex = Terminal(self.tmp, 'Op. Igual', self.tipo[-1])
                        list_lex.append(objlex)
                        self.limpieza()
                    else:
                        self.limpieza()
                    self.i-=1

            elif self.edo == 6:                                
                if c == "=":
                    self.edo = 0
                    self.tmp +=c
                    self.tipo.append(7)
                    objlex = Terminal(self.tmp, 'Op. Relacional', self.tipo[-1])
                    list_lex.append(objlex)
                    self.limpieza()
                
                elif c == " ":
                    self.edo = 0

                elif c == "~":
                    self.edo = 0
                    self.tipo.append(7)
                    objlex = Terminal(self.tmp, 'Op. Relacional', self.tipo[-1])
                    list_lex.append(objlex)
                    self.continua = False
                else:
                    self.edo = 0
                    self.tipo.append(7)
                    objlex = Terminal(self.tmp, 'Op. Relacional', self.tipo[-1])
                    list_lex.append(objlex)
                    self.limpieza()
                    self.i-=1

            elif self.edo == 7:                              
                if c == "|":
                    self.edo = 0
                    self.tmp +=c
                    self.tipo.append(8)
                    objlex = Terminal(self.tmp, 'Op. Or', self.tipo[-1])
                    list_lex.append(objlex)
                    self.limpieza()
                
                elif c == " ":
                    self.edo = 0

                elif c == "~":
                    
                    self.continua = False
                else:
                    self.edo = 0
                    self.limpieza()
                    self.i-=1

            elif self.edo == 8:                                
                if c == "&":
                    self.edo = 0
                    self.tmp +=c
                    self.tipo.append(9)
                    objlex = Terminal(self.tmp, 'Op. And', self.tipo[-1])
                    list_lex.append(objlex)
                    self.limpieza()
                
                elif c == " ":
                    self.edo = 0

                elif c == "~":
                    
                    self.continua = False
                else:
                    self.edo = 0
                    self.limpieza()
                    self.i-=1
            
            elif self.edo == 9:                               
                if c == "'" or c == '"':
                    self.edo = 0
                    self.tmp +=c
                    self.tipo.append(3)
                    objlex = Terminal(self.tmp, 'Cadena', self.tipo[-1])
                    list_lex.append(objlex)
                    self.limpieza()
                

                elif c == "~":
                    
                    self.continua = False
                else:
                    self.edo = 9
                    self.tmp +=c
                    

            self.i+=1

        self.edo = 0
        self.i = 0
        self.tmp =""
        self.continua = True
        bandera =0
        

    def reservado(self):
        strid = self.tmp
        if "while" == strid:
            self.tipo.append(20)
            objlex = Terminal(self.tmp, 'Ciclo', self.tipo[-1])
            list_lex.append(objlex)

        elif "if" == strid:
            self.tipo.append(19)
            objlex = Terminal(self.tmp, 'Condicional', self.tipo[-1])
            list_lex.append(objlex)

        elif "return" == strid:
            self.tipo.append(21)
            objlex = Terminal(self.tmp, 'Retorno', self.tipo[-1])
            list_lex.append(objlex)

        elif "else" == strid:
            self.tipo.append(22)
            objlex = Terminal(self.tmp, 'Condicional', self.tipo[-1])
            list_lex.append(objlex)

        elif "int" == strid:
            self.tipo.append(4)
            objlex = Terminal(self.tmp, 'Tipo', self.tipo[-1])
            list_lex.append(objlex)

        elif "float" == strid:
            self.tipo.append(4)
            objlex = Terminal(self.tmp, 'Tipo', self.tipo[-1])
            list_lex.append(objlex)

        elif "void" == strid:
            self.tipo.append(4)
            objlex = Terminal(self.tmp, 'Tipo', self.tipo[-1])
            list_lex.append(objlex)

        elif "print" == strid:
            self.tipo.append(0)
            objlex = Terminal(self.tmp, 'Impresion', self.tipo[-1])
            list_lex.append(objlex)

        else:        
            self.tipo.append(0)
            objlex = Terminal(self.tmp, 'Identificador', self.tipo[-1])
            list_lex.append(objlex)
            if globals()['ban_lex']==0:
                flag =0
                try:
                    if list_lex[-2].tipo== 'Tipo':
                        
                        try:
                            if (self.cadena_analizada[self.i]) == ';':            
                                
                                pass
                            elif (self.cadena_analizada[self.i]) == ',':            
                                
                                pass
                            elif len(list_lex)>2: 
                                if (list_lex[2].cad) == '(' and ')' in self.cadena_analizada:           
                                    
                                    pass
                                elif ')' in self.cadena_analizada:
                                    pass
                                else:
                                    flag =1


                            if flag ==1:
                                if (self.cadena_analizada[self.i]) == '(':           
                                    flag = 0
                                    pass
                                    
                                else:
                                    print('No hay')
                                    list_er_lex.append('Punto y coma faltantes: '+  str(list_lex[-2].cad) + ' '+ self.tmp)
                                    print(len(list_er_lex))

                        except:
                            pass
                    
                except: 
                    pass
                aumento = 2
                aux = 0
                if list_lex[-1].tipo== 'Identificador':
                    if entrada[actual + 1]=='=':
                        if ';' in entrada[actual + 2]:
                            pass
                        else:
                            aumento +=1
                            if entrada[actual + aumento] == '+' or entrada[actual + aumento] == '-' or  entrada[actual + aumento] == '*' or entrada[actual + aumento] == '/':
                                while aux == 0:
                                    if entrada[actual + aumento] == '+' or entrada[actual + aumento] == '-' or  entrada[actual + aumento] == '*' or entrada[actual + aumento] == '/':
                                        aumento +=1
                                        if ';' in entrada[actual + aumento]:
                                            aux =1
                                            globals()['ban_lex']=0
                                            break
                    
                                        cadena2 = analizador(entrada[actual + aumento])
                                        globals()['ban_lex']=1
                                        cadena2.anlexico()
                                        if list_lex[-1].pos == 0 or list_lex[-1].pos == 1 or list_lex[-1].pos == 2:
                                            aumento +=1
                                            list_lex.pop()
                                        else:
                                            aux =1
                                            list_lex.pop()
                                            list_er_lex.append('Punto y coma faltantes: '+   str(entrada[actual]) + str(entrada[actual + 1]) + str(entrada[actual + 2]))
                                            break
                                    else:
                                        aux =1
                                        list_lex.pop()
                                        list_er_lex.append('Punto y coma faltantes: '+   str(entrada[actual]) + str(entrada[actual + 1]) + str(entrada[actual + 2]))
                                        break
                            else:
                                temp = actual +1
                                error = 0
                                while True:
                                    if ');' in entrada[temp]:
                                        error =0
                                        break
                                    if ')' in entrada[temp]:
                                        error =1
                                        break
                                    else:
                                        temp +=1       
                                if error ==1:
                                    list_er_lex.append('Punto y coma faltantes: '+   str(entrada[actual]) + str(entrada[actual + 1]) + str(entrada[actual + 2]))
            else:
                pass          

    def analizadorsintactico(self, i, auxelimna2, entrada2):
        while True:
            for obj in lista_pila:
                try:
                    pass
                except:
                    pass
            if entrada2[i]=='print':
                globals()['valorprint']= entrada[i+2]
                globals()['banderaprint']=1
                
                i+=4
            fila = lista_pila[-1].pos
            
            columna = buscar_lex(entrada2[i])
            accion = matr_regl[fila][columna.pos]
            accion= Estado(str(accion), accion, accion, accion)
            if accion.estado == 0:
                print('Error')
                globals()['rev_error'] = 1
                break
            elif accion.estado > 0:
                i+=1
                lista_pila.append(columna)
                lista_pila.append(accion)
            elif accion.estado  <0:
                if accion.estado == -1:
                    break
                else:
                    for obj in list_reglas:
                        if accion.estado == (obj.aux +1) * -1:
                            accion = matr_regl[fila][obj.num]
                            accion= Estado(str(accion), accion, accion, accion)
                            if obj.elementos !=0:
                                eliminar = obj.elementos *2
                                self.buscaregla(obj.aux, eliminar)
                                fila = lista_pila[-1].pos
                                accion = matr_regl[fila][obj.num]   
                                lista_pila.append(obj.regla)
                                accion= Estado(str(accion), accion, accion, accion)
                                lista_pila.append(accion)
                            else:
                                if obj.aux == 10 :
                                    globals()['cont']=lista_pila[-4].cad
                                    code.primer_trad(10, globals()['cont'])
                                elif obj.aux == 12:
                                    z = 0
                                    posi =2
                                    posfi = 6
                                    if lista_pila[2]=='Definicion':
                                        while z == 0: 
                                            posi = posi +2
                                            if lista_pila[posi] == 'Definicion':
                                                posfi = posfi +2
                                            else:
                                                globals()['cont'] =lista_pila[posfi].cad
                                                z = 1
                                                break
                                    else:
                                        globals()['cont']= lista_pila[4].cad
                                    code.primer_trad(12, globals()['cont'])
                                lista_pila.append(obj.regla)
                                lista_pila.append(accion)
                            break
                        
                
    def buscaregla(self, num, cantidad):
        if num == 1:                        
            programa = Programa('Data')
            programa.programaexitoso()
        elif num == 3:                          
            if len(list_definiciones)==0:
                definiciones = Definiciones('Data', 'Data')
                definiciones.eliminaDefiniciones()
            else:
                definiciones = Definiciones('Data', list_def[-1])
                definiciones.eliminaDefiniciones()
        elif num == 4:                              
            definicion = Definicion('Data',lista_variables[-1])
            definicion.eliminaDefVar()
        elif num == 5:                             
            if len(lista_funciones)==0:
                definicion = Definicion('Data')
                definicion.eliminaDef()
            else:
                definicion = Definicion('Data', lista_funciones[-1])
                definicion.eliminaDef()
            list_def_loc.clear()
            list_def_locales.clear()
        
        elif num == 6:                          
            defvar = Definicion_Var('Data','Data','Data')
            defvar.eliminaVar()

        elif num == 8:                                             
            defvar = Definicion_Var('Data','Data','Data')
            defvar.eliminalistaVar()
        elif num == 9:                                                 
            deffun =Definicion_Funcion('Data', 'ID', 'Tipo')
            deffun.eliminaFunc()
        elif num == 11:                                            
            defpara = Parametros('Data','Id','Tipo')
            defpara.eliminaPara()
        elif num == 12:
            pass
        elif num == 13:                                             
            defpara = Parametros('Data','Id','Tipo')
            defpara.eliminalistaPara()
        elif num == 14:                                                
            bloquefun = Bloque_Funcion('Data', 0)
            bloquefun.eliminaBlo()
        elif num == 16:                                                
            if len(list_def_locales)==0:
                deflocales = Definicion_Locales('Data')
                deflocales.eliminaDef()
                list_def_locales.append(deflocales)
            else:
                auxiliar = list_def_locales[-1]
                auxiliar.eliminaDef()
        elif num == 17:                                                
            if len(list_def_loc)==0:
                deflocal = Definicion_Local('Data')
                deflocal.eliminaVar()
                list_def_loc.append(deflocal)
            else:
                auxiliar = list_def_loc[-1]
                auxiliar.eliminaVar()
        elif num == 18:                                                
            deflocal = Definicion_Local('Data')
            deflocal.eliminaSen()
            list_def_expr.clear()
        elif num == 20:
            sentencia = Sentencia('Data', 'Sentencias')
            sentencia.eliminaSentencias()
        elif num == 21:                                             
            sentencia = Sentencia('Data', 'Sentencia')
            sentencia.eliminaSen()
        elif num == 22:
            sentencia = Sentencia('Data', 'Sentencia If')
        elif num == 23:
            sentencia = Sentencia('Data', 'Sentencia While')
        elif num == 24:
            sentencia = Sentencia('Data', 'Sentencia')
            sentencia.eliminavalor()
            
        elif num == 28:
            bloquefun = Bloque_Funcion('Data', 1)
            bloquefun.eliminaBloque()

        elif num == 30: 
            lista_pila.pop()
            lista_pila.pop()
            tipo = ''
            contexto  = ''
            i = 0
            posi =2
            posfi = 6
            if lista_pila[2]=='Definicion':
                while i == 0: 
                    posi = posi +2
                    if lista_pila[posi] == 'Definicion':
                        posfi = posfi +2
                    else:
                        contexto =lista_pila[posfi].cad
                        i = 1
                        break
            else:
                contexto= lista_pila[4].cad
            if list_term[-1].tipo == 'Real':
                tipo = 'float'
            elif list_term[-1].tipo == 'Entero':
                tipo = 'int'
            elif list_term[-1].tipo == 'Identificador':
                for obj in list_param_id:
                    if list_term[-1].cad == obj.id and contexto == obj.tipo:
                        tipo = obj.data
                if tipo == '':
                    for obj in lista_variables:
                        if list_term[-1].cad == obj.tipo.cad and contexto == obj.lv:
                            tipo = obj.data.cad
                            break
                    
            else:
                tipo = list_term[-1].tipo
            globals()['tipo_ret'] = tipo
            llist_ret.append(Retorno(list_term[-1].cad, tipo, contexto))
            code.trad_ret(list_term[-1].cad, contexto)
        elif num == 32:
            argumento = Argumentos('Data') 
            argumento.eliminaarg()

        elif num == 34:
            argumento = Argumentos('Data') 
            argumento.eliminalistaarg()
        elif num == 35:
            terminoid = Termino('Data', 'Tipo', 'Lv')
            terminoid.eliminaTerminoLlamada()
        elif num == 36:                         
            terminoid = Termino('Data', 'Tipo', 'Lv')
            terminoid.eliminaTerminoId()
        elif num == 37:
            terminoid = Termino('Data', 'Tipo', 'Lv')
            terminoid.eliminaTerminoEntero()
        elif num == 38:
            terminoid = Termino('Data', 'Tipo', 'Lv')
            terminoid.eliminaTerminoFloat()
        elif num == 40:                     
            llamada = Llamada_Funcion('Data', 'Funcion')
            llamada.eliminallamada()
        elif num == 42:                    
            sentencia = Sentencia('Data', 'Sentencia Bloque')
            sentencia.eliminaSentenciaBloque()
        elif num == 46:                               
            expresion = Expresion('Data')
            expresion.eliminaMul()
        elif num == 47:                               
            expresion = Expresion('Data')
            expresion.eliminaSum()
        
        elif num == 48:
            expresion = Expresion('Data')
            expresion.eliminarelacional()
        elif num == 52:                                      
            if len(list_def_expr)==0:
                expresion = Expresion('Data')
                expresion.eliminaTer()
                list_def_expr.append(expresion)
            else:
                auxiliar = list_def_expr[-1]
                auxiliar.eliminaTer()
        else:
            while cantidad != 0:
                lista_pila.pop()
                cantidad-=1
                                    
    def limpieza(self):
        self.edo = 0
        self.tmp =""
        self.continua = True


entrada = " int var1;\
        int multiplicacion(int var1, int var2){\
        return var1 * var2;\
        }\
        int main(){\
        int var2;\
        int var4;\
        int var5;\
        var2 = 8;\
        var4 = 4;\
        var5 = multiplicacion(var2, var4);\
        print(var5)\
        }"

entrada = entrada.split()
entrada.append("$")
actual = 0
for i in range (len(entrada)):
    actual = i
    cadena = analizador(entrada[i])
    cadena.anlexico()
if globals()['ban_p']!=0:
    list_er_lex.append('Error, falta cerrar parentesis ')
if globals()['ban_c']!=0:
    list_er_lex.append('Error, falta cerrar corchetes ')
list_entrada = list()
print('\nAnalizador Léxico')
#print('Entrada', f"{'':>9}", 'Tipo', f"{'':>9}", 'Token', f"{'':<9}")
#print("-----------------------------------------------")
data = []
band = 0
for objlex in list_lex:
    #print(objlex.cad, f"{'-':>11}", objlex.tipo, f"{'-':>9}", objlex.pos)
    if objlex.cad == "$":
        data.append([objlex.cad, objlex.tipo, objlex.pos])
        band = 1
    if band == 0:
        data.append([objlex.cad, objlex.tipo, objlex.pos])
    list_entrada.append(objlex.cad)
print(tabulate(data, headers=["Entrada", "Tipo", "Token"]))
entrada.clear()    
entrada=list_entrada
auxelimna = (len(entrada)-2)*2
fila = 0
columna = 0
accion =0
acept = False
print(len(list_er_lex))
if len(list_er_lex)!=0:
    for obj in list_er_lex:
        print(obj)
        pass
else:
    lista_pila.append(buscar_lex("$"))
    lista_pila.append(Estado("0",0,0,0))
    rev_regl()
    auxil_regl()
    cadena.analizadorsintactico(0, auxelimna, entrada)

print("\n\n\t\tArbol Sintáctico")
if len(list_er)!=0:
    for obj in list_er:
        print(obj)
else:
    for pre, fill, node in RenderTree(raiz):
        print("%s%s" % (pre, node.name))

    print('\n\n Analizador Semántico')
    print('Tipo Dato', f"{'':>4}", 'Variable', f"{'':>5}", 'Seccion', f"{'':<11}")
    print('-----------------------------------')
    for obj in lista_variables:
        print(obj.data.cad, f"{'|':>11}", obj.tipo.cad, f"{'|':>9}", obj.lv)
    print("\n\n\t\tCodigo Ensamblador")
    code.gettraduccion()


    