import os, pty, serial
import io
import time

class Robot_mock:
    def __init__(self):
        self.listo=True
        pass
    def read(self):
        pass
    def espera_prompt(self):
        pass
    def write(self, comando):
        pass
    def reset(self):
        pass
    def prepara_siguiente_cara(self):
        pass
    def fin_escaneo(self):
        pass

class Robot:

    def __init__(self):
        self.tty = '/dev/ttyUSB0'
        self.serial = serial.Serial(self.tty, timeout=0.01)

        self.count = 0
        self.listo = False
        self.reset()


    def read(self):
        self.line = self.serial.readline()
        while 'robik$ ' not in self.line:
            self.count = self.count+1
            self.line = self.serial.readline()
            if not self.line:
                break

    def espera_prompt(self):
        self.line = ''
        while self.line <> 'robik$ ':
            time.sleep(0.01)
            self.line = self.serial.readline()

    def write(self, cmd):
        self.espera_prompt()
        self.serial.write(cmd + '\r')


    def reset(self):
        self.carasescaneadas=0

    def fin_escaneo(self):
        time.sleep(0.3)
        self.write('gb 1')

    def apoya_cubo(self):
        self.write('m0') # muneca a 30
        self.write('gb')    # grua abajo
        time.sleep(0.2)
        self.write('pm')    # pinza abierta
        time.sleep(0.1)

    def traslacionX(self):
        self.apoya_cubo()
        self.write('tx 1')

    def prepara_siguiente_cara(self):
        self.listo = False
        print "Preparo cara ",self.carasescaneadas
        if self.carasescaneadas == 0:
            pass
        if self.carasescaneadas == 1:
            self.traslacionX()
        elif self.carasescaneadas == 2:
            self.traslacionX()
        elif self.carasescaneadas == 3:
            self.apoya_cubo()
            self.write('pa')
            time.sleep(0.1)
            self.write('ba 1')
            self.traslacionX()
        elif self.carasescaneadas == 4:
            self.apoya_cubo()
            self.write('pa')
            time.sleep(0.1)
            self.write('ba 1')
            self.traslacionX()
            self.traslacionX()
        elif self.carasescaneadas == 5:
            self.traslacionX()

        self.carasescaneadas = self.carasescaneadas + 1
        time.sleep(1)
        self.listo = True

    def prepara_siguiente_cara_rapido(self):
        self.listo = False
        print "Preparo cara ",self.carasescaneadas
        if self.carasescaneadas == 0:
            self.write('pm')      # pinza a la mitad
            self.write('sm 150')  # muneca a 150 grados
            time.sleep(0.3)
            self.write('pc')      # cierra pinza
            time.sleep(0.3)
            self.write('gu')      # grua arriba
            time.sleep(0.3)
            self.write('sm 180')  # muneca a 180 grados
        if self.carasescaneadas == 1:
            self.write('m1')  # muneca a 90 grados
        elif self.carasescaneadas == 2:
            self.write('m0')  # muneca a 0 grados
        elif self.carasescaneadas == 3:
            self.write('sm 60') # muneca a 30
            time.sleep(0.3)
            self.write('gb')    # grua abajo
            time.sleep(0.3)
            self.write('pm')    # grua abajo
            time.sleep(0.3)

            self.write('m1') # muneca a 30
            self.write('pc')
            time.sleep(0.3)
            self.write('gu')
            time.sleep(0.3)
            self.write('m0')
            time.sleep(0.3)
            self.write('gb')
            time.sleep(0.3)


            self.write('pm')    # pinza abierta
            self.write('sm 150')  # muneca a 150 grados
            time.sleep(0.3)
            self.write('gb -1')  # gira la base 1
            time.sleep(0.3)
            self.write('pc')      # cierra pinza
            time.sleep(0.3)
            self.write('gu')      # grua arriba
            time.sleep(0.3)
            self.write('sm 180')  # muneca a 180 grados
        elif self.carasescaneadas == 4:
            self.write('m1')  # muneca a 90 grados
        elif self.carasescaneadas == 5:
            self.write('m0')  # muneca a 0 grados

        self.carasescaneadas = self.carasescaneadas + 1
        self.listo = True


