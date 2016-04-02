import os, pty, serial
import io
import time
import random

"""
Patrones
http://ruwix.com/the-rubiks-cube/rubiks-cube-patterns-algorithms/
"""

class Patrones:

    def __init__(self):
        self.patrones = [("Superflip", " U R2 F B R B2 R U2 L B2 R U' D' R2 F R' L B2 U2 F2 "),
            ("El ajedrez", " F B2 R' D2 B R U D' R L' D' F' R2 D F2 B' "),
            ("El ajedrez facil", " L2 R2 U2 D2 F2 B2 "),
            ("Spiral ", " L' B' D U R U' R' D2 R2 D L D' L' R' F U "),
            ("Logo de speedsolving.com", " R' L' U2 F2 D2 F2 R L B2 U2 B2 U2 "),
            ("Bandas verticales", " F U F R L2 B D' R D2 L D' B R2 L F U F "),
            ("Esquinas opuestas", " R L U2 F2 D2 F2 R L F2 D2 B2 D2 "),
            ("Cruz", " U F B' L2 U2 L2 F' B U2 L2 U"),
            ("Cruz 2", " R2 L' D F2 R' D' R' L U' D R D B2 R' U D2"),
            ("Cubo en cubo", " F L F U' R U F2 L2 U' L' B D' B' L2 U"),
            ("Cubo en cubo en cubo", " U' L' U' F' R2 B' R F U B2 U B' L U' F U R F'"),
            ("Anaconda", " L U B' U' R L' B R' F B' D R D' F'"),
            ("Python", " F2 R' B' U R' L F' L F' B D' R B L2"),
            ("Black Mamba", " R D L F' R L' D R' U D' B U' R' D'"),
            ("Green Mamba", " R D R F R' F' B D R' U' B' U D2"),
            ("Four spots", " F2 B2 U D' R2 L2 U D'"),
            ("Six spots", " U D' R L' F B' U D'"),
            ("Twister", " F R' U L F' L' F U' R U L' U' L F'"),
            ("Center-Edge-Corner", " F B2 R' D2 B R U D' R L' D' F' R2 D F2 B' U D' R L' F B' U D'"),
            ("Tetris", " L R F B U' D' L' R'"),
            ("Henry's Zig Zag with Checkerboard", " R2 L2 F2 B2 U F2 B2 U2 F2 B2 U"),
            ("Facing Checkerboards", " U2 F2 U2 F2 B2 U2 F2 D2 ")
            ]

    def elige_al_azar(self):
        self.patron = random.sample(self.patrones, 1)[0]

    def get_nombre(self):
        return self.patron[0]

    def get_secuencia(self):
        res = self.patron[1]
        return res.replace(" ",'')

    def get_secuencia_inversa(self):
        res = self.patron[1] + " "
        rev = ""
        for r in reversed(res.split(' ')):
            rev = rev + r + " "

        for m in 'LRUDFB':
            rev = rev.replace(m + " ",m + "# ") # auxiliar
            rev = rev.replace(m + "' ",m + " ")
            rev = rev.replace(m + "# ",m + "' ")
        return rev.replace(" ",'')

    def limpia_secuencia(self, sec):
        return sec.replace(" ",'')


class Robot:

    def __init__(self):
        self.tty = '/dev/ttyUSB0'
        #self.serial = serial.Serial(self.tty, timeout=0.01)

    def read(self):
        self.line = self.serial.readline()
        while 'robik$ ' not in self.line:
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


if __name__ == "__main__":

    r = Robot()
    p = Patrones()
    while True:
        p.elige_al_azar()

        print "\n\n\n"
        print "--------------------------------------------------------------------------------"
        print "  Robik demo - patrones.py"
        print "--------------------------------------------------------------------------------"
        print "   " + p.get_secuencia()
        print "       (retrocedo con : " + p.get_secuencia_inversa() + ")"

        r.write('seq ' + p.get_secuencia())
        r.write('pa')                                                                                         
        r.write('ba 4')                                                                                       
        r.write('pa')                                                                                         
        r.write('ba -4')     
        time.sleep(10);
        r.write('seq ' + p.get_secuencia_inversa())
        r.write('pa')                                                                                         
        r.write('ba 4')                                                                                       
        r.write('pa')                                                                                         
        r.write('ba -4')     
        time.sleep(5);


