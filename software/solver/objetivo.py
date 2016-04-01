import random
from cubo import *
from secuencia import *
import time
import sys

MAX_SEQ_CRUZ = 9
MAX_SEQ_SLOT = 11
MAX_SEQ_OLL  = 15
MAX_SEQ_PLL  = 999

def notation(moves):
    faces = 'UBRFLD'
    res = ''

    if type(moves)==list and moves:
        if type(moves[0][0])==list:
            res = ''
            for x in moves:
                res = res+notation(x)
            return res
            
    for m in moves:
        s = faces[m[0]]
        if m[1] == 3:
            n = ''
        elif m[1] == 2:
            n = '2'
        else:
            n = '\''
        res = res+s+n
    return res
        

class Estado:

    def __init__(self, cubo):
        self.cubo = cubo
        self.secuencia = []
        self.mejor_solucion = []
        pass

    def aplica(self, mov):
        # A veces la solucion tiene 0 movs
        if not mov:
            return
        if type(mov[0]) == list:
            for x in mov:
                self.aplica(x)
        elif type(mov)== str:
            S = Secuencia()
            self.aplica(S.secuencia_to_list(mov))
        elif mov:
            self.cubo.move(mov[0],mov[1])
            self.secuencia.append(mov)
        #print self.cubo.toStr()
        #print "secuencia : ",self.secuencia
        #print indent,"Estado = ",self.cubo.valor,'  secuencia = ',self.secuencia

    def toStr(self):
        s = self.cubo.toStr()
        s = s + "secuencia actual = " + notation(self.secuencia)
        return s
        
    def undo(self, mov):
        if not mov:
            return

        if type(mov[0]) == list:
            mov.reverse()
            for m in mov:
                self.undo(m)
        else:
            last = self.secuencia.pop()
            #print "undo. Ahora secuencia = ",self.secuencia
            self.cubo.move(last[0],4-last[1])
            #print indent,"(undo) Estado = ",self.cubo.valor,'  secuencia = ',self.secuencia


class Objetivo(object):

    """Docstring for Objetivo. """

    def __init__(self, estado, name = "Sin nombre!"):
        self.name = name
        self.estado = estado
        self.estado.secuencia = []
        self.starttime = time.time()
        self.duracion = 0
        self.algunasolucion = False
        pass
    def completado(self):
        self.duracion = time.time() - self.starttime


class ObjetivoUltimoGiro(Objetivo):

    """Docstring for Objetivopll. """

    def __init__(self, estado):
        """TODO: to be defined1. """
        Objetivo.__init__(self, estado, "UltimoGiro")
        self.secuencia = Secuencia()
        self.max_len_secuencia = 1

    def completado(self):

        for c in range(6):
            if [x.value for x in self.estado.cubo.caras[c].aristas] <> [c,c,c,c] or \
                    [x.value for x in self.estado.cubo.caras[c].esquinas] <> [c,c,c,c]:
                        return False
        self.algunasolucion = True
        return True

    def movs_posibles(self):
        return [[1,1],[1,2],[1,3]]
        
    def poda(self):
        return len(self.estado.secuencia)>1


class ObjetivoPLL(Objetivo):

    """Docstring for Objetivopll. """

    def __init__(self, estado):
        """TODO: to be defined1. """
        Objetivo.__init__(self, estado, "PLL")
        self.secuencia = Secuencia()
        self.max_len_secuencia = MAX_SEQ_PLL + 1

        self.movimientos_posibles = self.lista_secuencias()

    def completado(self):
        Objetivo.completado(self)
        for n in range(6):
            c = self.estado.cubo.caras[n].centro.value
            if [x.value for x in self.estado.cubo.caras[n].aristas] <> [c,c,c,c] or \
               [x.value for x in self.estado.cubo.caras[n].esquinas] <> [c,c,c,c]:
                return False

        self.algunasolucion = True
        return True

        c = self.estado.cubo.caras[5]
        if (c.aristas[2].value<>c.esquinas[2].value or c.esquinas[2].value<>c.esquinas[3].value):
            return False
        c = self.estado.cubo.caras[2]
        if (c.aristas[1].value<>c.esquinas[1].value or c.esquinas[1].value<>c.esquinas[2].value):
            return False
        c = self.estado.cubo.caras[4]
        if (c.aristas[0].value<>c.esquinas[0].value or c.esquinas[0].value<>c.esquinas[1].value):
            return False
        c = self.estado.cubo.caras[3]
        if (c.aristas[3].value<>c.esquinas[0].value or c.esquinas[0].value<>c.esquinas[3].value):
            return False

        return True

    def anade_combinaciones(self, lista, secuencia):
        # Las secuencias son siempre para la cara de arriba

        lista.append('X2'+secuencia)
        lista.append('X2Y' + secuencia)
        lista.append('X2Y2' + secuencia)
        lista.append("X2Y'" + secuencia)

    def movs_posibles(self):
       if len(self.estado.secuencia)==0:
           return self.movimientos_posibles
       else:
           return [[5,1],[5,2],[5,3]]  # cara de arriba

    # TODO borrar esto?
    def movs_posibles_mal(self):
        return self.movimientos_posibles
        
    def lista_secuencias(self):
        lista_combinaciones = []
        #http://rubiksolucion.blogspot.com.es/2013/07/pll-oll-f2l.html

        """
        self.anade_combinaciones(lista_combinaciones,"FRUR'U'F'") #1
        self.anade_combinaciones(lista_combinaciones,"fRUR'U'f'") #4
        self.anade_combinaciones(lista_combinaciones,"RUR'URU2R'") # 35
        self.anade_combinaciones(lista_combinaciones,"RU2R'U'RU'R'") # 
        """
        self.anade_combinaciones(lista_combinaciones,"U") #Puede que solo haga falta un giro
        self.anade_combinaciones(lista_combinaciones,"XR'UR'D2RU'R'D2R2") #1
        self.anade_combinaciones(lista_combinaciones,"X'RU'RD2R'URD2R2") #2
        self.anade_combinaciones(lista_combinaciones,"RU'RURURU'R'U'R2") #3
        self.anade_combinaciones(lista_combinaciones,"R2URUR'U'R'U'R'UR'") #4
        self.anade_combinaciones(lista_combinaciones,"M2UM2U2M2UM2") #5
        self.anade_combinaciones(lista_combinaciones,"RUR'U'R'FR2U'R'U'RUR'F'") #6
        self.anade_combinaciones(lista_combinaciones,"RUR'F'RUR'U'R'FR2U'R'U'") #7
        self.anade_combinaciones(lista_combinaciones,"FRU'R'U'RUR'F'RUR'U'R'FRF'") #8
        self.anade_combinaciones(lista_combinaciones,"R'U2RU2R'FRUR'U'R'F'R2U'") #9
        self.anade_combinaciones(lista_combinaciones,"LU2L'U2LF'L'U'LULFL2U") #10
        self.anade_combinaciones(lista_combinaciones,"R'UR'd'R'F'R2U'R'UR'FRF") #11
        self.anade_combinaciones(lista_combinaciones,"R'U2R'd'R'F'R2U'R'UR'FRU'F") #12
        self.anade_combinaciones(lista_combinaciones,"RUR'Y'R2u'RU'R'UR'uR2") 
        self.anade_combinaciones(lista_combinaciones,"R'U'RYR2uR'URU'Ru'R2") #13
                                                      
        self.anade_combinaciones(lista_combinaciones,"R2u'RU'RUR'uR2YRU'R'") 
        self.anade_combinaciones(lista_combinaciones,"R2uR'UR'U'Ru'R2Y'R'UR")
        self.anade_combinaciones(lista_combinaciones,"M2UM2UM'U2M2U2M'U2") 
        self.anade_combinaciones(lista_combinaciones,"R'UL'U2RU'R'U2RLU'")
        self.anade_combinaciones(lista_combinaciones,"X'RU'R'DRUR'D'RUR'DRU'R'D'") #1
        self.anade_combinaciones(lista_combinaciones,"R'UL'U2RU'LR'UL'U2RU'LU'") #1
        self.anade_combinaciones(lista_combinaciones,"LU'RU2L'UR'LU'RU2L'UR'U") #1


        l = []
        index = 0
        for x in lista_combinaciones:
            index = index + 1
            l.append(self.secuencia.secuencia_to_list(x))

        return l

    def poda(self):
        return len(self.estado.secuencia)>MAX_SEQ_PLL


class ObjetivoOLL(Objetivo):

    """Docstring for ObjetivoOll. """

    def __init__(self, estado):
        """TODO: to be defined1. """
        Objetivo.__init__(self, estado, "OLL")
        self.secuencia = Secuencia()
        self.max_len_secuencia = MAX_SEQ_OLL + 1

        self.movimientos_posibles = self.lista_secuencias()

    def completado(self):
        Objetivo.completado(self)

        c = self.estado.cubo.caras[2]
        color2 = c.centro.value
        aristas2 = [c.aristas[0].value, c.aristas[2].value, c.aristas[3].value]
        esquinas2 = [c.esquinas[0].value, c.esquinas[3].value]
        # Tienen que coincidir las aristas/esquinas alejadas de la cara de arriba
        if aristas2 <> [color2,color2,color2] or esquinas2 <> [color2,color2]:
            print "Color 2 = ",color2,"  Aristas:",aristas2, "  esquinas",esquinas2
            return False

        c = self.estado.cubo.caras[3]
        color3 = c.centro.value
        aristas3 = [c.aristas[0].value, c.aristas[1].value, c.aristas[3].value]
        esquinas3 = [c.esquinas[0].value, c.esquinas[1].value]
        if aristas3 <> [color3,color3,color3] or esquinas3 <> [color3,color3]:
            print "Color 3 = ",color3,"  Aristas:",aristas3, "  esquinas",esquinas3
            return False


        c = self.estado.cubo.caras[4]
        color4 = c.centro.value
        aristas4 = [c.aristas[0].value, c.aristas[1].value, c.aristas[2].value]
        esquinas4 = [c.esquinas[1].value, c.esquinas[2].value]

        if aristas4 <> [color4,color4,color4] or esquinas4 <> [color4,color4]:
            print "Color 4 = ",color4,"  Aristas:",aristas4, "  esquinas",esquinas4
            print "esqunas todas son: ",c.esquinas[0].value,c.esquinas[1].value,c.esquinas[2].value,c.esquinas[3].value
            print self.estado.cubo.toStr()
            return False

        c = self.estado.cubo.caras[1]
        color1 = c.centro.value
        aristas1 = [c.aristas[2].value, c.aristas[1].value, c.aristas[3].value]
        esquinas1 = [c.esquinas[2].value, c.esquinas[3].value]
        if aristas1 <> [color1,color1,color1] or esquinas1 <> [color1,color1]:
            return False

        c = self.estado.cubo.caras[5]
        color5 = c.centro.value
        aristas5 = [x.value for x in self.estado.cubo.caras[5].aristas]
        esquinas5 = [x.value for x in self.estado.cubo.caras[5].esquinas]
        if aristas5 <> [color5,color5,color5,color5] or esquinas5 <> [color5,color5,color5,color5]:
            return False

        self.algunasolucion = True
        return True

    def anade_combinaciones(self, lista, secuencia):
        # Las secuencias son siempre para la cara de arriba

        lista.append('X2'+secuencia)
        lista.append('X2Y' + secuencia)
        lista.append('X2Y2' + secuencia)
        lista.append("X2Y'" + secuencia)

    def movs_posibles(self):
        return self.movimientos_posibles
        
    def lista_secuencias(self):
        lista_combinaciones = []
        #http://rubiksolucion.blogspot.com.es/2013/07/pll-oll-f2l.html

        """
        self.anade_combinaciones(lista_combinaciones,"FRUR'U'F'") #1
        self.anade_combinaciones(lista_combinaciones,"fRUR'U'f'") #4
        self.anade_combinaciones(lista_combinaciones,"RUR'URU2R'") # 35
        self.anade_combinaciones(lista_combinaciones,"RU2R'U'RU'R'") # 
        """

        self.anade_combinaciones(lista_combinaciones,"FRUR'U'F'") #1
        self.anade_combinaciones(lista_combinaciones,"FRUR'U'RUR'U'F'") #
        self.anade_combinaciones(lista_combinaciones,"YR'U'RU'R'URU'R'U2R")
        self.anade_combinaciones(lista_combinaciones,"fRUR'U'f'") #4
        self.anade_combinaciones(lista_combinaciones,"fRUR'U'RUR'U'f'")
        self.anade_combinaciones(lista_combinaciones,"f'L'U'LUf")
        self.anade_combinaciones(lista_combinaciones,"F'L'U'LUL'U'LUF")
        self.anade_combinaciones(lista_combinaciones,"FRUR'U'F'UFRUR'U'F'")
        self.anade_combinaciones(lista_combinaciones,"YrUR'UR'FRF'RU2r'") #9
        self.anade_combinaciones(lista_combinaciones,"fRUR'U'f'UFRUR'U'F'")
        self.anade_combinaciones(lista_combinaciones,"fRUR'U'f'U'FRUR'U'F'") #11
        self.anade_combinaciones(lista_combinaciones,"FRUR'U'F'fRUR'U'f'") #12
        self.anade_combinaciones(lista_combinaciones,"fRUR'U'f'FRUR'U'F'") #13
        self.anade_combinaciones(lista_combinaciones,"rUr'RUR'U'rU'r'") #14
        self.anade_combinaciones(lista_combinaciones,"l'U'lL'U'LUl'Ul") # 15
        self.anade_combinaciones(lista_combinaciones,"R'FRUR'U'F'UR") #
        self.anade_combinaciones(lista_combinaciones,"RUR'U'M'URU'r'") # 17
        self.anade_combinaciones(lista_combinaciones,"MURUR'U'M2URU'r'") # 
        self.anade_combinaciones(lista_combinaciones,"FRUR'U'RF'rUR'U'r'") # 19
        self.anade_combinaciones(lista_combinaciones,"RUR'U'R'FRF'") # 
        self.anade_combinaciones(lista_combinaciones,"rUR'U'r'FRF'") # 
        self.anade_combinaciones(lista_combinaciones,"F'rUR'U'r'FR") # 
        self.anade_combinaciones(lista_combinaciones,"R'U'R'FRF'UR") # 
        self.anade_combinaciones(lista_combinaciones,"RU2R'R'FRF'U2R'FRF'") # 
        self.anade_combinaciones(lista_combinaciones,"RU2R'R'FRF'RU2R'") # 
        self.anade_combinaciones(lista_combinaciones,"MURUR'U'M'R'FRF'") # 
        self.anade_combinaciones(lista_combinaciones,"R'FR'F'R2U2YR'FRF'") # 
        self.anade_combinaciones(lista_combinaciones,"RUR'URU'R'U'R'FRF'") #  28
        self.anade_combinaciones(lista_combinaciones,"L'U'LU'L'ULULF'L'F") # 
        self.anade_combinaciones(lista_combinaciones,"R'U'RU'R'dR'URB") # 
        self.anade_combinaciones(lista_combinaciones,"RUR'UR'FRF'U2R'FRF'") # 
        self.anade_combinaciones(lista_combinaciones,"FRUR'UF'Y'U2R'FRF'") # 
        self.anade_combinaciones(lista_combinaciones,"r'U2RUR'Ur") # 
        self.anade_combinaciones(lista_combinaciones,"rUR'URU2r'") # 
        self.anade_combinaciones(lista_combinaciones,"RUR'URU2R'") # 35
        self.anade_combinaciones(lista_combinaciones,"RU2R'U'RU'R'") # 
        self.anade_combinaciones(lista_combinaciones,"R'FRF'R'FRF'RUR'U'RUR'") # 
        self.anade_combinaciones(lista_combinaciones,"RUR'URU2R'FRUR'U'F'") #  38
        self.anade_combinaciones(lista_combinaciones,"rUR'URU'R'URU2r'") # 
        self.anade_combinaciones(lista_combinaciones,"l'U'LU'L'ULU'L'U2l") # 
        self.anade_combinaciones(lista_combinaciones,"rU2R'U'RU'r'") # 
        self.anade_combinaciones(lista_combinaciones,"FRU'R'U'RUR'F'") #  42
        self.anade_combinaciones(lista_combinaciones,"r'U'RU'R'U2r") # 
        self.anade_combinaciones(lista_combinaciones,"M'UMU2M'UM") # 
        self.anade_combinaciones(lista_combinaciones,"RUR'U'XD'R'URU'DX'") # 
        self.anade_combinaciones(lista_combinaciones,"FURU'R2F'RURU'R'") # 
        self.anade_combinaciones(lista_combinaciones,"R'FRUR'F'RY'RU'R'") # 47
        self.anade_combinaciones(lista_combinaciones,"R2DR'U2RD'R'U2R'") # 
        self.anade_combinaciones(lista_combinaciones,"R'U2R2UR'URU2X'U'R'U") # 
        self.anade_combinaciones(lista_combinaciones,"RdL'd'R'URBR'") #  50
        self.anade_combinaciones(lista_combinaciones,"Y2L'd'RdLU'L'B'L") # 
        self.anade_combinaciones(lista_combinaciones,"RB'R'U'RUBU'R'") # 
        self.anade_combinaciones(lista_combinaciones,"R'FR2B'R2F'R2BR'") # 
        self.anade_combinaciones(lista_combinaciones,"RUR'U'RU'R'F'U'FRUR'") # 
        self.anade_combinaciones(lista_combinaciones,"R2UR'B'RU'R2URBR'") #  55
        self.anade_combinaciones(lista_combinaciones,"R'U'RY'X'RU'R'FRUR'") # 
        self.anade_combinaciones(lista_combinaciones,"RUR'YR'FRU'R'F'R") # 

        l = []
        for x in lista_combinaciones:
            l.append(self.secuencia.secuencia_to_list(x))

        return l

    def poda(self):
        return len(self.estado.secuencia)>MAX_SEQ_OLL


class ObjetivoSlot(Objetivo):

    """Docstring for ObjetivoSlot. """

    def __init__(self, estado, slots_completos = []):
        """TODO: to be defined1. """
        Objetivo.__init__(self, estado, "Slot siguiente")
        self.color_centro = self.estado.cubo.caras[0].centro.value
        self.slots_completos = slots_completos
        self.set_siguiente_slot()
        # Me quedo con las aristas actuales, que no pueden variar
        self.aristas = [x.value for x in self.estado.cubo.caras[0].aristas]
        self.last_move = None    # Guardo el tipo de movimiento MOV_ARRIBA
        self.it = 0
        self.log = ''
        self.max_len_secuencia = MAX_SEQ_SLOT

    def set_siguiente_slot(self):
        """ 
        Decide el mejor slot, con unas heuristicas sencillas (de hecho, sin ella actualmente)
        """
        for i in range(4):
            if i not in self.slots_completos:
                # Get laterales de slot
                self.slot_actual=i

                # Las caras implicadas en cada slot se corresponden al numero del slot + 1, y su anterior
                #
                self.cara_1 = i + 1
                self.cara_2 = i % 4
                if self.cara_2 == 0:
                    self.cara_2 = 4


                # Los colores implicadas en el slot son los adyacentes a las aristas de la cruz implicadas
                # TODO: sobra esto. ahora Son los mismos colores!
                self.color_1 = self.estado.cubo.caras[self.cara_1].centro
                self.color_2 = self.estado.cubo.caras[self.cara_2].centro

                # print "Colores implicados: ", self.color_1.value, self.color_2.value

                # La arista debe quedar con estos colorese:
                self.arista_slot_ok = [self.color_1.value, self.color_2.value]

                """
                Dado un slot, con color_1 y color_2 hay  saber que elemento de lista de aristas tengo
                que comprobar en cada cara. El slot 0 lo forman la cara NORTE y la anterior en el sentido
                de las agujas del reloj (oeste). El slot 1 lo forman la cara ESTE y la anterior...etc
                Segun la representacion planar del cubo se comprueba que la orientacion del segundo color
                siempre es igual al slot, y la del primer color la anterior
                Ej: Slot 0:   Cara norte y Cara oeste      Indice 1: OESTE     Indice 2: NORTE
                    Slot 1:   Cara este  y Cara norte      Indice 1: NORTE     Indice 2: ESTE
                    Slot 2:   Cara sur   y Cara este       Indice 1: ESTE      Indice 2: SUR
                    Slot 3:   Cara oeste y Cara sur        Indice 1: SUR       Indice 2: OESTE
                """
                self.indice_arista_1 = (self.slot_actual - 1) % 4
                self.indice_arista_2 = self.slot_actual 

                # print "Los indices serian:", self.indice_arista_1, self.indice_arista_2

                """
                Las esquinas son parecidas a las aristas, teniendo en cuenta que hay dos elementos para
                cada orientacion (dos al norte, dos al este...). Al primer indice le sumamos 1
                Ej: Slot 0:   Cara norte           Cara oeste
                              Indice 1: SUR + 1    ESTE
                """

                self.indice_esquina_1 = (self.slot_actual + 3) % 4  # +2(=contrario) +1
                self.indice_esquina_2 = (self.slot_actual + 1) % 4  # (el anterior)
                # La esquina tiene los mismos colores que la arista + el de la cruz
                self.esquina_slot_ok = self.arista_slot_ok + [self.estado.cubo.caras[0].centro.value]

                # print "Los indices esquina serian:", self.indice_esquina_1, self.indice_esquina_2
                # Localiza la arista del slot
                #self.cara_slot_1 = self.estado.cubo.caras[self.estado.cubo.caras[0].centrosad[cara1].value]
                #self.cara_slot_2 = self.estado.cubo.caras[self.estado.cubo.caras[0].centrosad[cara2].value]

                # Localiza la posicion de las esquinas
                # 
                # Para el slot 0 tengo que pillar la arista Este de la cara Norte
                # Para el slot 1 tengo que pillar la arista 
                self.slot_secuencia=[]
                self.len_secuencia_anterior = len(self.estado.secuencia)
                self.max_len_secuencia = MAX_SEQ_SLOT
                break

    def completado(self):
        Objetivo.completado(self)

        """
        El slot esta completado cuando:
        1. Las aristas siguen formando cruz
        2. La esquina tiene los colores de la cara de la cruz + los dos colores de las caras
           del slot. Para la orientacion solo hay que comprobar uno de los colores (en este
           caso, solo compruebo que el color correspondiente a la cruz este bien orientado
        3. Cada arista tiene sus dos colores en la cara correspondiente
        """

        aristas = [x.value for x in self.estado.cubo.caras[0].aristas]

        cara=self.estado.cubo.caras  # por claridad
        arista_slot_actual = [cara[self.cara_1].aristas[self.indice_arista_1].value, \
                              cara[self.cara_2].aristas[self.indice_arista_2].value]

        esquina_slot_actual= [cara[self.cara_1].esquinas[self.indice_esquina_1].value, \
                              cara[self.cara_2].esquinas[self.indice_esquina_2].value, \
                              cara[0].esquinas[self.slot_actual].value]

        if (arista_slot_actual == self.arista_slot_ok) and \
           (esquina_slot_actual == self.esquina_slot_ok) and \
               (aristas == self.aristas):

            self.algunasolucion = True
            if self.slot_actual not in self.slots_completos:
                self.slots_completos.append(self.slot_actual)
            return True
        
        return False


    def movs_posibles(self):
        """
        Los pasos para hacer un slot siguen esta secuencias (puede empezar en 1)
        0. paso inicial (si las piezas del slot no esta arriba)
            0.1 mover cara de arriba o cualquiera de los laterales
            0.2 saltar al paso 2
        1. Move una de las caras laterales del slot
        2. Mover la cara de arriba
        3. Deshacer el movimiento de la cara lateral
        4. Mover la cara de arriba
        5. saltar al paso 1
        """
        l = []

        len_secuencia = len(self.estado.secuencia)

        # Ningun tipo de euristica

        if len_secuencia==0:
            # Inicialmente, calculo ya las caras que no debo mover porque desharian slots hechos 
            self.movs_prohibidos=[]
            for x in self.slots_completos:
                self.movs_prohibidos.append([x+1,3])
                if x == 0:
                    x2 = 4
                else:
                    x2 = x
                self.movs_prohibidos.append([x2,1])

            for j in range(1,5):  # caras laterales
                if [j,1] not in self.movs_prohibidos:
                    l.append([j,1])
                if [j,3] not in self.movs_prohibidos:
                    l.append([j,3])
            for j in range(1,4): # cara de arriba
                l.append([5,j])

        else:
            last_move = self.estado.secuencia[len(self.estado.secuencia)-1][0]
            if last_move<>5:
                for j in range(1,4): # cara de arriba
                    l.append([5,j])

            else:
                # Cuantos movimientos laterales hubo?
                movs_laterales = [x for x in self.estado.secuencia if x[0]<>5]
                if len(movs_laterales)%2 == 0:
                    if (len(movs_laterales)<4):
                        # Estoy colocando lo que deshice
                        for j in range(1,5):  # caras laterales
                            if last_move <> j:
                                if [j,1] not in self.movs_prohibidos:
                                    l.append([j,1])
                                if [j,3] not in self.movs_prohibidos:
                                    l.append([j,3])
                    else:
                        # Muevo solo el slot. Solo tiene sentido un giro determinado para cada cara
                        s = self.cara_1
                        if last_move <> s:
                            l.append([s,3])
                        s = self.cara_2
                        if last_move <> s:
                            l.append([s,1])
                else:
                    ultimo_mov = movs_laterales[len(movs_laterales)-1]
                    l.append([ultimo_mov[0],4-ultimo_mov[1]])
                
        return l


    def poda(self):
        if len(self.estado.secuencia)-self.len_secuencia_anterior > self.max_len_secuencia:
            return True
        else:
            return False


class ObjetivoCruz(Objetivo):

    """Docstring for ObjetivoCruz. """

    def __init__(self, estado):
        """TODO: to be defined1. """
        Objetivo.__init__(self, estado, name = "Cruz")
        # El objetivo incluye que las aristas de la cruz esten ordenadas
        # Solo lo hago una vez
        self.orden=[x.value for x in self.estado.cubo.caras[0].centrosad]
        self.color_centro = self.estado.cubo.caras[0].centro.value

        # Va controlando el numero de ordenados
        self.update_ordenadas()
        self.max_len_secuencia=MAX_SEQ_CRUZ

    def completado(self):
        Objetivo.completado(self)
        global str_solucion
        if self.ordenadas==5:
            self.algunasolucion = True
            return True
        else:
            return False

    def movs_posibles(self):
        l = []
        if self.ordenadas == 4: # ultimo movimiento
            for j in range(3):
                l.append([0,j+1])
        else:
            for i in range(6):
                if self.estado.secuencia and self.estado.secuencia[len(self.estado.secuencia)-1][0] == i:
                    # No repito el mismo mov
                    pass
                else:
                    blancas_en_i = [x.value for x in self.estado.cubo.caras[i].aristas if x.value == self.color_centro ] 
                    blancas_ady_en_i = [x.value for x in self.estado.cubo.caras[i].aristasad if x.value == self.color_centro ] 
                    if blancas_en_i or blancas_ady_en_i:
                        for j in range(3):
                            l.append([i,j+1])

        return l

    def update_ordenadas(self):
        aristasad = [x.value for x in self.estado.cubo.caras[0].aristasad]
        aristas0 = [x.value for x in self.estado.cubo.caras[0].aristas]
        pares = zip(aristasad,aristas0)
        colores = [x if y==self.color_centro else -1 for x,y in pares]
        self.ordenadas=0
        for i in range(4):
            z = zip(colores,self.orden)
            iguales = [x for x in z if x[0]==x[1]]
            self.ordenadas = max(self.ordenadas, len(iguales))
            colores = colores[1:] + colores[:1]
        if (self.ordenadas == 4):
            if colores == self.orden:
                self.ordenadas = 5

    def poda(self):
        len_secuencia = len(self.estado.secuencia)
        if len_secuencia > self.max_len_secuencia:
            return True

        self.update_ordenadas()
        
        if len_secuencia == 6:
            # al menos 3 colocadas!
            return self.ordenadas<3
        elif len_secuencia == 5:
            return self.ordenadas<3
        elif len_secuencia == 4:
            return self.ordenadas<2
        elif len_secuencia == 3:
            return self.ordenadas<2
        elif len_secuencia == 2:
            return self.ordenadas<1
        return False
        
