import random

COLOR_WHITE = 0
COLOR_BLUE = 1
COLOR_RED = 2
COLOR_GREEN = 3
COLOR_ORANGE = 4
COLOR_YELLOW = 5

NORTE = 0
ESTE = 1
SUR = 2
OESTE = 3


# http://stackoverflowcom/questions/287871/print-in-terminal-with-colors-using-python.
class fg:
    black = '\033[30m'
    red = '\033[31m'
    green = '\033[32m'
    orange = '\033[33m'
    blue = '\033[34m'
    purple = '\033[35m'
    cyan = '\033[36m'
    lightgrey = '\033[37m'
    darkgrey = '\033[90m'
    lightred = '\033[91m'
    lightgreen = '\033[92m'
    yellow = '\033[93m'
    lightblue = '\033[94m'
    pink = '\033[95m'
    lightcyan = '\033[96m'

class Color(object):
    """Representa un color, entendido como una "pegatina" del cubo
    Existen 9*6 pegatinas, y cada cara apunta a estas pegatinas
    """

    CSI = "\x1B["
    reset = CSI+"m"

    unicode_square = u"\u2588"
    def __init__(self, color):
        """TODO: to be defined1. """
        color = int(color)
        if type(color) is not int:
            raise Exception("Errooooor","mensaje")
        else:
            self.value = color

    def __getitem__(self):
        return self.value

    def toNombre(self):
        if self.value == 0:
            return "blanco "
        elif self.value == 1:
            return "amarillo "
        elif self.value == 2:
            return "rojo "
        elif self.value == 3:
            return "naranja "
        elif self.value == 4:
            return "azul "
        else:
            return "verde "

    def toStr(self):
        if self.value == 0:
            ascii = u"\u2588" + " "
        else:
            if self.value == 1:
                ascii = fg.blue
            elif self.value == 2:
                ascii = fg.red
            elif self.value == 3:
                ascii = fg.green
            elif self.value == 4:
                ascii = fg.pink
            elif self.value == 5:
                ascii = fg.yellow
            ascii = "\x1b[" + ascii + u"\u2588" + "\x1B[m" + " "
        return ascii



class Lista4(object):

    """
    Objeto auxiliar : lista de 4 colores
    Representa:
        los colores de las 4 esquinas que tiene una cara
        los colores de las 4 aristas que tiene una cara
        los colores de 4 esquinas que tienen las caras adyacentes a una cara
        los colores de 4 aristas que tienen las caras adyacentes a una cara
        ... siempre en grupos que se ven implicados en cada giro
    """

    static_dboid = 0

    def __init__(self, c1, c2, c3, c4):
        """Construye el objto con una lista de 4 colores """

        Lista4.static_dboid=Lista4.static_dboid + 1
        self.dboid=Lista4.static_dboid
        self.colores = [c1, c2, c3, c4]

    def toStr(self):
        res = ''
        for i in self.colores:
            res = res + i.toStr()
        return res

    def __getitem__(self, index):
        return self.colores[index]

    def rotate(self, clockwise=True):
        if clockwise:
            aux = self.colores[0].value
            for i in range(3):
                self.colores[i].value = self.colores[i+1].value
            self.colores[3].value = aux
        else:
            aux = self.colores[3].value
            for i in range(2,-1,-1):  # 2,1,0
                self.colores[i+1].value = self.colores[i].value
            self.colores[0].value = aux


class Cara(object):

    """
    Modela la cara de un cubo.
    Tiene 1 centro, 4 esquinas, 4 aristas y 4 caras adyacentes
    """

    def __init__(self, color):
        """Construyo la cara de un color, especificando ademas los colores adyacentes """
        self.centro = Color(color)
        self.esquinas = Lista4(Color(color), Color(color), Color(color), Color(color))
        self.aristas = Lista4(Color(color), Color(color), Color(color), Color(color))

    def setColores(self, e0,a0,e1,a3,c,a1,e3,a2,e2):
        self.centro = Color(c)
        self.aristas = Lista4(Color(a0), Color(a1), Color(a2), Color(a3))
        self.esquinas = Lista4(Color(e0), Color(e1), Color(e2), Color(e3))

    """
    Configura los adjacentes a una cara. Los indices tienen esta esctructura:
        0  0  1  Es decir, aristas y esquinas independientes, numeradas clockwise
        3     1  comenzando en la esquina superior derecha.
        3  2  2

    El offset sirve para indicar
    Por ejemplo, en una representacion plana del cubo:
        B
      O W R Y
        G
    Consideramos offset 0 el caso de la cara W (blanca). 
    La esquina W0 (empareja con B3 (el tres de su cara norte)
    R0 empareja con B2, en su cara norte (offset -1)
    """

    def setAdyacentes(self, ady, indexes):

        self.nseo = indexes;

        self.esquinasad1 = Lista4(ady[0].esquinas[indexes[0]],
                                ady[1].esquinas[indexes[1]],
                                ady[2].esquinas[indexes[2]],
                                ady[3].esquinas[indexes[3]])
        self.aristasad = Lista4(ady[0].aristas[indexes[0]],
                                ady[1].aristas[indexes[1]],
                                ady[2].aristas[indexes[2]],
                                ady[3].aristas[indexes[3]])
        self.esquinasad2 = Lista4(ady[0].esquinas[(indexes[0]+1)%4],
                                ady[1].esquinas[(indexes[1]+1)%4],
                                ady[2].esquinas[(indexes[2]+1)%4],
                                ady[3].esquinas[(indexes[3]+1)%4])
        """
        Los centros, en el estado inicial, tienen el mismo color que las aristas.
        No entran en la rotacion, pero los apunto para controlar su orden
        cuando estoy haciendo la cruz, ya que las aristasad van cambiando
        """
        self.centrosad = Lista4(ady[0].centro,
                                ady[1].centro,
                                ady[2].centro,
                                ady[3].centro)
        


    def get_color_en(self, nseo):
        return self.centrosad[nseo]

    def rotate(self, clockwise = True):
        self.esquinas.rotate(clockwise)
        self.aristas.rotate(clockwise)
        self.esquinasad1.rotate(clockwise)
        self.esquinasad2.rotate(clockwise)
        self.aristasad.rotate(clockwise)

    def strC(self, color):
        return color.toStr()

    def toStr(self,fila):
        if fila == 0:
            res = self.strC(self.esquinas[0]) + \
                  self.strC(self.aristas[0]) + \
                  self.strC(self.esquinas[1])
        elif fila == 1:
            res = self.strC(self.aristas[3]) + \
                  self.strC(self.centro) + \
                  self.strC(self.aristas[1])
        elif fila == 2:
            res = self.strC(self.esquinas[3]) + \
                  self.strC(self.aristas[2]) + \
                  self.strC(self.esquinas[2])
        return res

class Cubo(object):

    """Representacion del cubo, con 6 caras
    Los colores son irrelevantes, y estan puestos a modo de ejemplo
    La cara 0 es en la que se hara la cruz
    La cara 5 es la contraria a la 0

              B B B                  0 0 1
              B 1 B                  3   1
              B B B                  3 2 2
        O O O W W W R R R Y Y Y
        O 4 O W 0 W R 2 R Y 5 Y
        O O O W W W R R R Y Y Y
              G G G
              G 3 G
              G G G
    """

    def __init__(self, blanca_arriba = True):
        """TODO: to be defined1. """

        # Creo una cara de cada color
        self.caras = []
        if blanca_arriba:
            self.caras.append(Cara(COLOR_WHITE))
            self.caras.append(Cara(COLOR_BLUE))
            self.caras.append(Cara(COLOR_RED))
            self.caras.append(Cara(COLOR_GREEN))
            self.caras.append(Cara(COLOR_ORANGE))
            self.caras.append(Cara(COLOR_YELLOW))
        else:
            caras = random.sample(range(6),6)
            #print caras
            for i in xrange(6):
                self.caras.append(Cara(caras[i]))

        self.configAdyacentes()

    def caracter2color(self,cadena, rotacion):
        res = ''
        colores = 'WYROBG'
        esquinas = [cadena[0:1],cadena[2:1],cadena[6:1],cadena[8:1]]
        aristas = [cadena[1:1],cadena[3:1],cadena[5:1],cadena[7:1]]
        centro = cadena[4:1]
        for x in range(rotacion):
            esquinas = esquinas[1:] + esquinas[0]
            aristas = aristas[1:] + aristas[0]
        for x in range(9):
            pass
            

    def setColoresCara(self, cara, lista, rotacion):

        print "Anadiendo a cara ",cara,lista,"con rotacion ",rotacion
        e0,a0,e1,a3,c,a1,e3,a2,e2 = lista
        print e0,a0,e1,a3,c,a1,e3,a2,e2,'ultimo'
        self.caras[cara].setColores(e0,a0,e1,a3,c,a1,e3,a2,e2)
        for i in xrange(rotacion):
            self.rotate(cara)

    def setCara(self, cara, cadena, rotacion):
        """
        FRBLUD
        ej: conColores(['GGOGGGOBY','YBGORWOOW','YYEFEREE'])
        """
        cadena2colores = []
        for x in range(9):
            cadena2colores.append('WYROBG'.index(cadena[x]))


        e = [cadena2colores[0],cadena2colores[2],cadena2colores[8],cadena2colores[6]]
        a = [cadena2colores[1],cadena2colores[5],cadena2colores[7],cadena2colores[3]]
        c = cadena2colores[4]

        for x in range(rotacion):
            e= e[1:] + [e[0]]
            a= a[1:] + [a[0]]

        print e,a
        self.caras[cara].setColores(e[0],a[0],e[1],a[3],c,a[1],e[3],a[2],e[2])




    def configAdyacentes(self):
        # Especifico adyacentes de cada cara
        """
        Especifico adyacentes a cada cara
        Cada cara tiene cuatro adyacentes, una al Norte, al Este... etc. Ademas, se especifica
        para cada adyacente cual la orientacion en la que se encuentra la cara origen.
        Por ejemplo: la cara WHITE tiene al norte la cara BLUE. Esta cara BLUE tiene la cara
        WHITE al sur.

        Los colores solo coincidirian en el caso base con la cruz blanca arriba. Se utilizan
        las constantes por claridad
        """
        self.caras[COLOR_WHITE].setAdyacentes([self.caras[COLOR_BLUE],
                                               self.caras[COLOR_RED],
                                               self.caras[COLOR_GREEN],
                                               self.caras[COLOR_ORANGE]],[SUR,OESTE,NORTE,ESTE])
        self.caras[COLOR_YELLOW].setAdyacentes([self.caras[COLOR_BLUE],
                                               self.caras[COLOR_ORANGE],
                                               self.caras[COLOR_GREEN],
                                               self.caras[COLOR_RED]],[NORTE,OESTE,SUR,ESTE])
        self.caras[COLOR_RED].setAdyacentes([self.caras[COLOR_BLUE],
                                               self.caras[COLOR_YELLOW],
                                               self.caras[COLOR_GREEN],
                                               self.caras[COLOR_WHITE]],[ESTE,OESTE,ESTE,ESTE])
        self.caras[COLOR_ORANGE].setAdyacentes([self.caras[COLOR_BLUE],
                                               self.caras[COLOR_WHITE],
                                               self.caras[COLOR_GREEN],
                                               self.caras[COLOR_YELLOW]],[OESTE,OESTE,OESTE,ESTE])
        self.caras[COLOR_BLUE].setAdyacentes([self.caras[COLOR_YELLOW],
                                               self.caras[COLOR_RED],
                                               self.caras[COLOR_WHITE],
                                               self.caras[COLOR_ORANGE]],[NORTE,NORTE,NORTE,NORTE])
        self.caras[COLOR_GREEN].setAdyacentes([self.caras[COLOR_WHITE],
                                               self.caras[COLOR_RED],
                                               self.caras[COLOR_YELLOW],
                                               self.caras[COLOR_ORANGE]],[SUR,SUR,SUR,SUR])

    

    def rotate(self, color, clockwise=True):
        self.caras[color].rotate(clockwise)

    def move(self, color, times):
        if times == 3:
            self.caras[color].rotate(False)
        elif times == 2:
            self.caras[color].rotate(False)
            self.caras[color].rotate(False)
        else:
            self.caras[color].rotate(True)

    def get_orientacion(self, caraorigen, caradestino):
        l = [x.value for x in caraorigen.centrosad]
        print "Orientacion para ",caraorigen.centro.value, caradestino.centro.value, l
        return l.index(caradestino.centro.value)

    def get_arista(self, cara, index):
        color1 = cara.aristas[index]
        cara_ad = cara.centrosad[index].value
        orientacion = self.get_orientacion(cara,self.caras[cara_ad])
        color2 = self.caras[cara_ad].aristas[orientacion]
        return (color1.value, color2.value)


    def toStr(self):
        res = ""
        res = res + "      " + self.caras[1].toStr(0) + "\n" \
                  + "      " + self.caras[1].toStr(1) + "\n" \
                  + "      " + self.caras[1].toStr(2) + "\n"
        res = res + self.caras[4].toStr(0) \
                  + self.caras[0].toStr(0) \
                  + self.caras[2].toStr(0) \
                  + self.caras[5].toStr(0) + "\n"
        res = res + self.caras[4].toStr(1) \
                  + self.caras[0].toStr(1) \
                  + self.caras[2].toStr(1) \
                  + self.caras[5].toStr(1) + "\n"
        res = res + self.caras[4].toStr(2) \
                  + self.caras[0].toStr(2) \
                  + self.caras[2].toStr(2) \
                  + self.caras[5].toStr(2) + "\n"
        res = res + "      " + self.caras[3].toStr(0) + "\n" \
                  + "      " + self.caras[3].toStr(1) + "\n" \
                  + "      " + self.caras[3].toStr(2) + "\n"


        res = res + "\n"

        return res

#c = Cubo()
#print c.toStr()
