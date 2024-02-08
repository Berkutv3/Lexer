
class Lexeme:
    def __init__(self,token,value):
        self.token = token
        self.value = value

class Lexer:
    reservarda = ["WHERE","AND","OR","NOT","where","and","or","not"]
    operadores = ["<",">","<=",">=","==","!=","&&","||","(",")","+","-","*","/","."]
    cadena = ""; buffer = ""; aux = ["",""]
    index = 0; i = 0; j = 0; token = 0; e_principal = 400
    
    MATRIZ_TRANSC_ID = [
        [1,-1,-1,-1],
        [1,2,3,4],
        [1,2,3,4],
        [1,2,3,4]
    ]
    
    MATRIZ_TRANSC_CONST = [
        [1,-1,3,-1,4],
        [1,2,5,5,5],
        [1,5,5,5,5],
        [3,3,5,3,3],
        [4,4,4,4,4,]
    ]
    
    def scaner_id(self,caracter):
        if caracter.isalpha():
            return 0
        elif caracter.isdigit():
            return 1
        elif caracter == '_':
            return 2
        else:
            return 3 
    
    def scaner_const(self,caracter):
        if caracter.isdigit():
            return 0
        elif caracter == '.':
            return 1
        elif caracter == '"':
            return 2
        elif caracter == "'":
            return 4
        else:
            return 3
    
    def checkfloat(self,x):
        c = ''
        for k in range(len(x)):
            c = x[k]
            if c == '.':
                return True
        return False
    
    def checkreserved(self):
        for i in range(2):
            if self.aux[i] == "":
                return False
        return True
    
    def buscar_reservada(self,simbolo):
        for i in range(7):
            if simbolo == self.reservarda[i]:
                return 100+i
        return 400
    
    def buscar_operador(self, simbolo):
        for i in range(15):
            if simbolo == self.operadores[i]:
                return 200+i
        return -666
    
    def afd_id(self):
        estado_actual = 0
        estado_sig = 0
        self.aux = ["",""]
        self.j = 0
        c = self.cadena[self.index]
        if not c.isalpha():
            return 300
        else:
            estado_sig = self.MATRIZ_TRANSC_ID[estado_actual][self.scaner_id(c)]
            while True:
                if estado_sig == 4:
                    self.j = 0
                    return 400
                else:
                    self.buffer += c
                    self.index += 1
                    self.token = self.buscar_reservada(self.buffer)
                    if not self.token == 400:
                        self.aux[self.j] = self.buffer
                        self.j += 1
                        self.buffer = ""
                    c = self.cadena[self.index]
                    estado_sig = self.MATRIZ_TRANSC_ID[estado_sig][self.scaner_id(c)]
                    self.buffer = self.buffer.strip()
    
    def afd_const(self):
        estado_actual = 0; estado_sig = 0; caracter = 0
        c = self.cadena[self.index]
        if not(c.isdigit()) and not(c == '"') and not(c == "'"):
            return 200
        else:
            estado_sig = self.MATRIZ_TRANSC_CONST[estado_actual][self.scaner_const(c)]
            if estado_sig == 4:
                caracter = 1
            while True:
                if (estado_sig == 5):
                    if not(self.checkfloat(self.buffer)) and not(c == '"') and not(c == "'"):
                        return 300
                    elif (self.checkfloat(self.buffer)) and not(c == '"') and not(c == "'"):
                        return 301
                    elif c == '"':
                        self.index += 1
                        self.buffer += c
                        return 303
                    elif c == "'" and len(self.buffer) > 1:
                        return 200
                else:
                    self.buffer += c
                    self.index += 1
                    c = self.cadena[self.index]
                    estado_sig = self.MATRIZ_TRANSC_CONST[estado_sig][self.scaner_const(c)]
                    self.buffer = self.buffer.strip()
                    if caracter == 1 and self.cadena[self.index + 1] == "'" and len(self.buffer) <= 1:
                        m = self.cadena[self.index]
                        self.buffer += m
                        self.index += 1
                        m = self.cadena[self.index]
                        self.buffer += m
                        self.index += 1
                        caracter = 0
                        return 302
                    if caracter == 1 and c == '"' and len(self.buffer) <= 1:
                        m = self.cadena[self.index]
                        self.buffer += m
                        self.index += 1
                        caracter = 0
                        return 302
                """
                if estado_sig == 5 and not(self.checkfloat(self.buffer)) and not(c == '"'):
                    return 300
                elif estado_sig == 5 and self.checkfloat(self.buffer) and not(c == '"'):
                    return 301
                elif estado_sig == 5 and c == '"':
                    self.index += 1
                    self.buffer += c
                    return 303
                else:
                    self.buffer += c
                    self.index += 1
                    c = self.cadena[self.index]
                    estado_sig = self.MATRIZ_TRANSC_CONST[estado_sig][self.scaner_const(c)]
                    self.buffer = self.buffer.strip()
                    if caracter == 1 and self.cadena[self.index + 1] == "'" and len(self.buffer) <= 1:
                        m = self.cadena[self.index]
                        self.buffer += m
                        self.index += 1
                        m = self.cadena[self.index]
                        self.buffer += m
                        self.index += 1
                        caracter = 0
                        return 302
                    elif caracter == 1 and c == '"' and len(self.buffer) <= 1:
                        m = self.cadena[self.index]
                        self.buffer += m
                        self.index += 1
                        caracter = 0
                        return 302
                    else:
                        return 200
                """

    def afd_simb(self):
        c = self.cadena[self.index]
        self.buffer += c
        self.token = self.buscar_operador(self.buffer)
        self.index += 1
        c = self.cadena[self.index]
        self.buffer += c
        self.token = self.buscar_operador(self.buffer)
        if self.token < 200 or self.token > 225:
            self.index -= 1
            c = self.cadena[self.index]
            self.buffer = ""
            self.buffer += c
            self.token = self.buscar_operador(self.buffer)
        return self.token
        
    def Analizar(self):
        l = Lexeme(0,"")
        while True:
            c = self.cadena[self.index]
            if c == '$':
                self.e_principal = -666
                l.token = -666
                l.value = c
                return l
            else:
                if c == ' ':
                    self.index += 1
                match self.e_principal:
                    case 400:
                        if self.checkreserved():
                            self.buffer = self.aux[self.j]
                            self.token = self.buscar_reservada(self.buffer)
                            l.value = self.buffer
                            self.buffer = ""
                            self.j += 1
                            if (self.j == 2):
                                self.aux = ["",""]
                            l.token = self.token
                            #print(l.value,"\t",l.token,"\n")
                            return l
                        else:
                            self.token = self.afd_id()
                            if self.token == 300:
                                self.e_principal = 300
                            elif not  self.checkreserved():
                                self.buffer = self.aux[0] + self.aux[1] + self.buffer
                                self.token = self.buscar_reservada(self.buffer)
                                l.value = self.buffer
                                self.buffer = ""
                                l.token = self.token
                                #print(l.value,"\t",l.token,"\n")
                                return l
                    case 300:
                        self.token = self.afd_const()
                        if (self.token == 200):
                            self.e_principal = 200
                        else:
                            l.value = self.buffer
                            self.buffer = ""
                            self.e_principal = 400
                            l.token = self.token
                            #print(l.value,"\t",l.token,"\n")
                            return l
                    case 200:
                        token = self.afd_simb()
                        if self.token == -666:
                            self.e_principal = -666
                        else:
                            l.value = self.buffer
                            self.buffer = ""
                            self.index += 1
                            self.e_principal = 400
                            l.token = token
                            #print(l.value,"\t",l.token,"\n")
                            return l
                    case -666:
                        if not self.buffer == "$":
                            self.e_principal = -1
                        else:
                            l.value = self.buffer
                            self.buffer = ""
                            l.token = self.token
                            #print(l.value,"\t",l.token,"\n")
                            return l
                    case -1:
                        print("Programa finalizo por error. Simbolos incorrectos\n")
                        l.token = self.token
                        return l
    
    def tipos(self, token):
        t = ""
        if token == 400:
            t = "Identificador\n"
        if token >= 200 and token <= 214:
            t = "Operador\n"
        if token >= 100 and token <= 107:
            t = "Palabra Reservada\n"
        if token >= 300 and token <= 303:
            t = "Constante\n"
        return t
        
    def LeerCadena(self,cadena):
        self.cadena = cadena + "$"
        print(cadena,"\n")
        TablaSimbolos = []
        while not (self.e_principal == -1 or self.e_principal == -666):
            TablaSimbolos.append(self.Analizar())
        for i in TablaSimbolos:
            print(i.token,"\t",i.value,"\t",self.tipos(i.token))
            

Analizador = Lexer()
cad = input("Cadena: ")
Analizador.LeerCadena(cad)
k = input("\nPress a key to close")    
    
    
    
    
