import random
from objetivo import *
from secuencia import *
import time
import logging
import sys


class Solver(object):

    """Docstring for Solver. """

    def __init__(self, cubo):

        self.solucion = list()                # Lista de movs que componen la solucion
        self.cubo = cubo
        self.estado = Estado(self.cubo)
        self.scramble_movs = []

        self.tiempos = list()                 # Lista de tiempos de cada paso (para estadisticas)
        self.tamanos = list()                 # Lista de tiempos de cada paso (para estadisticas)
        self.lasttime = 0

        self.running = False

        self.secuencias = []
        self.status = ""

        pass

    def get_secuencia(self):
        if self.secuencias:
            next = self.secuencias[0]
            self.secuencias = self.secuencias[1:]
            return next
        else:
            return None

    def is_running(self):
        return self.running

    def set_status(self, status):
        if self.status:
            self.status = self.status + '\n' + status
        else:
            self.status = status

    def get_status(self):
        tmp = self.status
        self.status = ""
        return tmp

    def scramble(self, veces):
        scramble = list()
        while True:
            cara,clock = [random.randint(0,5),random.randint(1,3)]
            if not scramble or scramble[len(scramble)-1][0]<>clock:
                self.cubo.move(cara,clock)
                scramble.append((cara,clock))
                veces = veces-1
            if veces == 0:
                break
        self.scramble_movs=scramble

    def solve_objetivo(self,objetivo, maxprof=999):
        self.buscaProf(objetivo, maxprof = maxprof)
        if not objetivo.algunasolucion:
            self.set_status("No encontre ninguna solucion!!!!")
            self.muestraStats(False)
            sys.exit(1)
        self.guardaStats(objetivo)
        if len(self.estado.mejor_solucion)>0:
            print objetivo.name, "solucion:" ,notation(self.estado.mejor_solucion)
            self.set_status(objetivo.name + " solucion:" + notation(self.estado.mejor_solucion) )
            self.estado.aplica(self.estado.mejor_solucion);
            self.solucion = self.solucion + self.estado.mejor_solucion
            self.secuencias.append(notation(self.estado.mejor_solucion))
            print self.estado.cubo.toStr()
        else:
            self.set_status(objetivo.name + " no necesita movimientos")


    def solve(self):
        self.running = True

        objetivo = ObjetivoCruz(self.estado)
        self.solve_objetivo(objetivo)

        # TODO: el estado debera tener los slots completos
        objetivo = ObjetivoSlot(self.estado, [])
        self.solve_objetivo(objetivo)
        objetivo = ObjetivoSlot(self.estado, objetivo.slots_completos)
        self.solve_objetivo(objetivo)
        objetivo = ObjetivoSlot(self.estado, objetivo.slots_completos)
        self.solve_objetivo(objetivo)
        objetivo = ObjetivoSlot(self.estado, objetivo.slots_completos)
        self.solve_objetivo(objetivo)

        objetivo = ObjetivoOLL(self.estado)
        self.solve_objetivo(objetivo, maxprof=0)

        objetivo = ObjetivoPLL(self.estado)
        self.solve_objetivo(objetivo, maxprof=1)

        self.muestraStats()
        self.running = False

    def guardaStats(self, objetivo):
        self.tiempos.append(objetivo.duracion)
        self.tamanos.append(len(self.estado.mejor_solucion))

    def muestraStats(self, haySolucion=True):

        print "--------------------------------------------------------------------------------"
        total=0
        for i in self.tiempos:
            total = total + i
        lista_tiempos = str( [round(x,2) for x in self.tiempos ] + [round(total,2)])
        lista_tamanos = str( [x for x in self.tamanos ] )
        print "Resumen:"
        print "Scramble = ",notation(self.scramble_movs)

        print "Solucion = ",notation(self.solucion),'  (',len(self.solucion),'movimientos )',' tiempos = ',lista_tiempos
        log = open('./log.txt','a')
        log.write ("016;"+str(lista_tiempos)+";"+str(lista_tamanos)+";"+notation(self.scramble_movs)+ \
                ";"+notation(self.solucion)+";"+str(len(self.solucion))+"\n")
        if not haySolucion:
            log.write ("Solucion no encontrada\n")


        log.close()
        print "--------------------------------------------------------------------------------"


    def buscaProf(self, objetivo, level=0, maxprof=99):

        if (objetivo.completado()):
            print "Objetivo",objetivo.name,"completado con",len(self.estado.secuencia),"movimientos. secuencia: ",notation(self.estado.secuencia)
            if len(self.estado.secuencia)<=objetivo.max_len_secuencia:
                objetivo.max_len_secuencia = len(self.estado.secuencia)-1
                self.estado.mejor_solucion = list(self.estado.secuencia)
        else:
            if level>maxprof:
                return
            movs = objetivo.movs_posibles()
            for i in movs:
                self.estado.aplica(i)

                if objetivo.poda():
                    pass
                else:
                    self.buscaProf(objetivo, level + 1, maxprof)

                self.estado.undo(i)


if __name__ == "__main__":
    c = Cubo(blanca_arriba = False)
    s = Solver(c)
    s.scramble(40)

    #s.estado.aplica("fRUR'U'f'U'FRUR'U'F'") # no encuentra sol para la cruz en 8
    print c.toStr()
    s.solve()
