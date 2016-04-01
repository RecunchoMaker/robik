class Secuencia(object):

    """Docstring for Secuencia. """

    def __init__(self, posicion=['U','B','R','F','L','D']):
        """TODO: to be defined1. """
        self.posicion_inicial = list(posicion)
        self.posicion = list(posicion)
        self.caras = list(posicion)

        self.traslacion = {}
        self.traslacion['X'] = ['F','U','B','D']
        self.traslacion['Y'] = ['F','L','B','R']
        self.traslacion['Z'] = ['U','R','D','L']

    def aplica_traslacion_lista(self, traslacion):
        res = []
        if len(traslacion)==4:
            traslacion.append(traslacion[0])
        for p in self.posicion:
            if p in traslacion:
                res.append(traslacion[traslacion.index(p)+1])
            else:
                res.append(p)
        self.posicion = res


    def mov_igual(self, mov):
        if mov[1] == '2' or mov[1] == '\'':
            ori = mov[1]
        else:
            ori = ''
        return mov[0] + ori

    def mov_contrario(self, mov):
        if mov[1] == '2':
            ori = '2'
        elif mov[1] == '\'':
            ori = ''
        else:
            ori = '\''
        return mov[0] + ori

    def normaliza_minusculas(self, secuencia):

        secuencia = secuencia + ' '
        pos = 0
        res = ''
        while pos < len(secuencia)-1:
            mov = secuencia[pos]
            ori = secuencia[pos + 1]
            if mov=='r':
                res=res + self.mov_igual('X'+ori) + self.mov_igual('L'+ori)
            elif mov=='l':
                res=res + self.mov_contrario('X'+ori) + self.mov_igual('R'+ori)
            elif mov=='u':
                res=res + self.mov_igual('Y'+ori) + self.mov_igual('D'+ori)
            elif mov=='d':
                res=res + self.mov_contrario('Y'+ori) + self.mov_igual('U'+ori)
            elif mov=='f':
                res=res + self.mov_igual('Z'+ori) + self.mov_igual('B'+ori)
            elif mov=='b':
                res=res + self.mov_contrario('Z'+ori) + self.mov_igual('F'+ori)
            else:
                res=res + self.mov_igual(mov+ori)

            pos = pos + 1
            if ori in "'2":
                pos = pos + 1

        return res


    def normaliza_traslaciones(self, secuencia):

        pos = 0
        res = ''
        secuencia = secuencia + ' '   # para evitar overflow en ori
        while pos<len(secuencia)-1:
            mov = secuencia[pos]
            ori = secuencia[pos+1]
            if mov in 'XYZ':
                traslacion_lista = list(self.traslacion[mov])
                if ori=='\'':
                    traslacion_lista.reverse()
                    pos = pos + 1
                self.aplica_traslacion_lista(traslacion_lista)
                if ori=='2':
                    self.aplica_traslacion_lista(traslacion_lista)
                    pos = pos + 1
            else:
                res = res + self.mov_igual(self.posicion_inicial[self.posicion.index(mov)]+ori)
                if ori in ' \'2':
                    pos = pos + 1

            pos = pos + 1

        return res.strip()

    def secuencia_to_list(self, secuencia):
        self.__init__()
        pos = 0
        res = []

        secuencia=secuencia.replace("M2","X2R2L2")
        secuencia=secuencia.replace("M'","XR'L")
        secuencia=secuencia.replace("M","X'RL'")
        secuencia = self.normaliza_minusculas(secuencia)

        secuencia = self.normaliza_traslaciones(secuencia)
        secuencia = secuencia + ' '   # para evitar overflow en ori
        while pos<len(secuencia)-1:
            mov = secuencia[pos]
            ori = secuencia[pos+1]
            if ori == '\'':
                clock = 1
                pos = pos + 1
            elif ori == '2':
                clock = 2
                pos = pos + 1
            else:
                clock = 3
            res.append([self.caras.index(mov),clock])
            pos = pos + 1
            
        return res


if __name__ == "__main__":
    s = Secuencia()
    #print s.posicion
    X = ['F','L','B','R']




