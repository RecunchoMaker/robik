import numpy as np

class CuboEscaneado:

    def __init__(self):

        self.carasescaneadas = 0
        self.colores = []
        self.colores_def = np.zeros([6,9])
        self.resultado = ""

    def get_resultado(self):
        return self.resultado

    def anadir_colores(self,colores) :
        self.carasescaneadas = self.carasescaneadas + 1
        self.colores.append(colores)

    def num_de_n_en_l(self, n, l):
        res = 0
        for i in l:
            if i==n:
                res = res + 1
        return res

    def numero_color(self, n, limites):
        if n<=limites[0]:
            return [0,'blanco  ']
        elif n<=limites[1]:
            return [4,'naranja ']
        elif n<=limites[2]:
            return [5,'amarillo']
        elif n<=limites[3]:
            return [3,'verde   ']
        elif n<=limites[4]:
            return [1,'azul    ']
        else:
            return [2,'rojo    ']

    def normaliza_colores(self):
        colores_norm = np.array(self.colores)
        # Desplazo el rojo si su H es muy alto
        for x in xrange(6):
            for y in xrange(9):
                if colores_norm[x][y]<4 and colores_norm[x][y]>=0:
                    colores_norm[x][y]=200

        n = colores_norm.copy()
        for i in n:
            print i
        n = n.reshape(54)

        # Desplazo el rojo si su H es muy alto
        for a in xrange(54):
            if n[a]<7 and n[a]>=0:
                print "d",
                n[a]=200
        n.sort()
        n = n.reshape((6,9))

        """
        print n
        print n[1]
        print n[1][2]
        """
        self.limit=[]
        for i in xrange(6):
            self.limit.append(n[i][8])
        print "limites = ",self.limit

        print "despues..."
        for i in n:
            print i
        self.colores_def = []
        for c in colores_norm:
            s = ""
            lista = []
            for d in c:
                nc = self.numero_color(d, self.limit)
                lista.append(nc[0])
                s = s + nc[1]
            self.colores_def.append(lista)

            print s
        centros = []
        aristas = []
        esquinas = []
        print self.colores_def
        for c in self.colores_def:
            print c
            centros.append(c[4])
            aristas.append(c[1])
            aristas.append(c[3])
            aristas.append(c[5])
            aristas.append(c[7])
            esquinas.append(c[0])
            esquinas.append(c[2])
            esquinas.append(c[6])
            esquinas.append(c[8])
        
        print "centros aristas y esquinas:"
        print centros
        print aristas
        print esquinas
        correcto = True
        for c in xrange(0,6):
            if self.num_de_n_en_l(c,centros)<>1:
                self.resultado = self.resultado + ("El color %d falla en los centros\n" % c)
                correcto = False
            elif self.num_de_n_en_l(c,aristas)<>4:
                self.resultado = self.resultado + ("El color %d falla en las aristas\n" % c)
                correcto = False
            elif self.num_de_n_en_l(c,esquinas)<>4:
                self.resultado = self.resultado + ("El color %d falla en las esquinas\n" % c)
                correcto = False
            print correcto
        if correcto:
            self.resultado = "Colores correctos"
        return correcto

